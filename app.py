import os
import unicodedata
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from utils import read_data, write_data

# Serve estáticos da pasta 'public'
app = Flask(__name__, static_folder='public', static_url_path='/public')

# Lista fixa de prédios
PREDIOS = [
    "PREDIO BAURU - LOTE 2",
    "PREDIO CAMPINAS SP - LOTE 2",
    "CENTRO ADM XAXIM - LOTE 2",
    "AG. 0348 - PREDIO FLORIANOPOLIS SC - LOTE 2",
    "PREDIO LONDRINA PR - LOTE 2",
    "PREDIO MOINHOS DE VENTO (AGENCIA R.OLAVO B VIANA-UPA) - LOTE 2",
    "CENTRO ADMINISTRATIVO PALACIO AVENIDA - LOTE 2",
    "PREDIO SAO JOSE DO RIO PRETO - LOTE 2",
]

# Colunas somente-leitura fixas (além de 'Sequencial' e da coluna de prédio)
BASE_READONLY = [
    "Pavimento",
    "Ambiente",
    "Tag do Equipamento",
    "Denominação do Equipamento",
]

# Colunas editáveis
EDITABLE = [
    "Fabricante",
    "Modelo",
    "Capacidade/Potência",
    "Nº SÉRIE",
    "Tipo de Gás Refrigerante",
    "Tensão de Trabalho (V)",
    "Data de Instalação",
    "Data de Fabricação",
    "Critico?",
]

def _normalize(s: str) -> str:
    """Remove acentos e retorna tudo em minúsculas."""
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('form',
                                predio=request.form['predio'],
                                idx=0))
    return render_template('index.html', predios=PREDIOS)

@app.route('/form', methods=['GET', 'POST'])
def form():
    predio = request.args.get('predio')
    idx    = int(request.args.get('idx', 0))

    # 1) Lê todos os dados da aba
    df_all = read_data()

    # 2) Detecta dinamicamente a coluna de prédio
    pr_col = next(
        (c for c in df_all.columns
         if isinstance(c, str) and 'predio' in _normalize(c)),
        None
    )
    if pr_col is None:
        raise KeyError("Coluna de prédio não encontrada no DataFrame.")

    # 3) Monta a lista de somente-leitura: Sequencial, Prédio, + BASE_READONLY
    readonly = ["Sequencial", pr_col] + BASE_READONLY

    # 4) Filtra apenas os ativos do prédio selecionado
    df = df_all[df_all[pr_col] == predio].reset_index()
    total = len(df)

    # Se já passou do último ativo, exibe a tela de conclusão
    if idx >= total:
        return render_template('done.html',
                               predio=predio,
                               total=total)

    if request.method == 'POST':
        # 5) Atualiza df_all: preenche "NA" em campos vazios
        for col in EDITABLE:
            field = (col.lower()
                     .replace(' ', '_')
                     .replace('/', '_')
                     .replace('(', '')
                     .replace(')', '')
                     .replace('?', ''))
            val = request.form.get(field, '').strip() or "NA"
            df_all.at[df.at[idx, 'index'], col] = val

        write_data(df_all)

        # 6) Navegação
        if 'next' in request.form:
            idx += 1
        elif 'prev' in request.form:
            idx -= 1
        idx = max(0, min(idx, total))
        return redirect(url_for('form',
                                predio=predio,
                                idx=idx))

    # 7) Renderiza o formulário do ativo atual
    record = df.iloc[idx].to_dict()
    return render_template('form.html',
                           predio=predio,
                           idx=idx,
                           total=total,
                           record=record,
                           readonly=readonly,
                           editable=EDITABLE)

@app.route('/restart')
def restart():
    return redirect(url_for('index'))

@app.route('/download')
def download():
    file_dir = os.path.join(os.path.dirname(__file__), 'data')
    filename = next(f for f in os.listdir(file_dir)
                    if f.lower().endswith('.xlsx'))
    return send_from_directory(file_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)