from flask import Flask, render_template, request

app = Flask(__name__)
ops = []
messages = []

@app.route('/', methods=["GET", "POST"])
def index():
    global ops, messages

    if messages == []:
        messages = [
            {"sender": "bot", "text": "Olá! Como posso ajudar?"}
        ]

    next_options = ["Tenho uma dúvida!"]

    # Responde solicitações de POST
    if request.method == "POST":
        selected_option = request.form.get("option")

        if selected_option:
            ops.append(selected_option)
            print(ops)

            # Árvore de respostas
            if ops == ['1']:
                messages.append({"sender": "user", "text": "Tenho uma dúvida!"})
                bot_message = "Ok! Estou aqui para ajudar. Escolha o tópico que gerou a dúvida:"
                next_options = ["Manifestação do Estado como Confrontante", "Validação de laudos",
                                "Voltar ao menu inicial"]

            # Manifestação do Estado como Confrontante
            elif ops == ['1', '1']:
                bot_message = "O que você quer saber sobre Manifestação do Estado como Confrontante?"
                next_options = ["O que é?", "Etapas"]

            elif ops == ['1', '1', '1']:
                bot_message = "A Manifestação de Confrontante deve ser solicitada quando ocorrer retificação de área ou pedido de usucapião que podem afetar terras ou imóveis públicos do Estado de Minas Gerais. Uma vez que imóveis públicos são inalienáveis, é fundamental ter a anuência do Estado nesses casos."
                next_options = ["Quero saber outra informação", "Voltar ao menu inicial"]

            elif ops == ['1', '1', '2']:
                bot_message = """
                Etapa 1: Reunir os seguintes documentos:<br>
                a) Lista de documentos:<br>
                b) Memorial Descritivo do imóvel;<br>
                c) Planta Topográfica Georreferenciada;<br>
                d) ART do responsável técnico;<br><br>
                Etapa 2: Enviar documentos por e-mail:<br>
                imoveis@planejamento.mg.gov.br 
                """
                next_options = ["Quero saber outra informação", "Voltar ao menu inicial"]

            elif ops == ['1', '1', '1', '1']:
                ops = ['1', '1']
                bot_message = "O que você quer saber sobre Manifestação do Estado como Confrontante?"
                next_options = ["O que é?", "Etapas"]

            elif ops == ['1', '1', '1', '2']:
                ops = ['1']
                bot_message = "Ok! Estou aqui para ajudar. Escolha o tópico que gerou a dúvida:"
                next_options = ["Manifestação do Estado como Confrontante", "Validação de laudos",
                                "Voltar ao menu inicial"]

            elif ops == ['1', '1', '2', '1']:
                ops = ['1', '1']
                bot_message = "O que você quer saber sobre Manifestação do Estado como Confrontante?"
                next_options = ["O que é?", "Etapas"]

            elif ops == ['1', '1', '2', '2']:
                ops = ['1']
                bot_message = "Ok! Estou aqui para ajudar. Escolha o tópico que gerou a dúvida:"
                next_options = ["Manifestação do Estado como Confrontante", "Validação de laudos",
                                "Voltar ao menu inicial"]

            # Validação de Laudos
            elif ops == ['1', '2']:
                bot_message = "O que você quer saber sobre Validação de laudos?"
                next_options = ["O que é?", "Etapas"]

            elif ops == ['1', '2', '1']:
                bot_message = """
                Procedimento pelo qual a SEPLAG/SCI valida um laudo de avaliação produzido por um terceiro. O laudo de avaliação validado pela SEPLAG/SCI é pré-requisito para os processos de autorização e permissão de uso, cessão de uso, entre outros. Para a validação do laudo ocorrer sem problemas, é preciso que o profissional que elabora o laudo:
                atenda as normas contidas no Decreto Estadual n°46.467, de 28/03/2014, e no Decreto Estadual nº 48.280, de 08/10/2021; 
                atenda as especificações exigidas pela NBR 14.653 (Norma Brasileira para Avaliação de Bens) em sua Parte 1 (Procedimentos Gerais - NBR 14.653-1 / Revisão 2019) e Parte 2 (Imóveis Urbanos - NBR 14.653-2 / Revisão 2011).
                De particular importância são os itens citados no item 9 - Apresentação do Laudo de Avaliação da NBR 14653-1:2019, que devem ser contemplados pelo laudo de avaliação. 
                """
                next_options = ["Quero saber outra informação", "Voltar ao menu inicial"]

            elif ops == ['1', '2', '2']:
                bot_message = """
                Etapa 1: Reunir os seguintes documentos:<br>
                a) identificação do solicitante do trabalho;<br>
                b) objetivo da avaliação;<br>
                c) finalidade da avaliação;<br>
                d) identificação e caracterização do bem avaliando;<br>
                e) documentação utilizada para a avaliação;<br>
                f) pressupostos e condições limitantes da avaliação;<br>
                g) dados e informações efetivamente utilizados;<br>
                h) memória de cálculo;<br>
                i) indicação do(s) método(s) utilizado(s), com justificativa da escolha;<br>
                j) especificação da avaliação; (quanto a grau de fundamentação e precisão);<br>
                k) resultado da avaliação e sua data de referência;<br>
                l) qualificação legal completa e assinatura do(s) responsável(is) técnico(s) pela avaliação;<br>
                m) local e data da elaboração do laudo;<br>
                n) fotos, e outros requisitos previstos nas demais partes da Norma.<br><br>
                Etapa 2: Enviar documentos por e-mail:<br>
                imoveis@planejamento.mg.gov.br
                """
                next_options = ["Quero saber outra informação", "Voltar ao menu inicial"]

            elif ops == ['1', '2', '1', '1']:
                ops = ['1', '1']
                bot_message = "O que você quer saber sobre Validação de Laudos?"
                next_options = ["O que é?", "Etapas"]

            elif ops == ['1', '2', '1', '2']:
                ops = ['1']
                bot_message = "Ok! Estou aqui para ajudar. Escolha o tópico que gerou a dúvida:"
                next_options = ["Manifestação do Estado como Confrontante", "Validação de laudos",
                                "Voltar ao menu inicial"]

            elif ops == ['1', '2', '2', '1']:
                ops = ['1', '1']
                bot_message = "O que você quer saber sobre Validação de Laudos?"
                next_options = ["O que é?", "Etapas"]

            elif ops == ['1', '2', '2', '2']:
                ops = ['1']
                bot_message = "Ok! Estou aqui para ajudar. Escolha o tópico que gerou a dúvida:"
                next_options = ["Manifestação do Estado como Confrontante", "Validação de laudos",
                                "Voltar ao menu inicial"]

            elif ops == ['1', '3']:
                ops = ['1']
                bot_message = "Ok! Estou aqui para ajudar. Escolha o tópico que gerou a dúvida:"
                next_options = ["Manifestação do Estado como Confrontante", "Validação de laudos",
                                "Voltar ao menu inicial"]

            # Manda as respostas
            messages.append({"sender": "bot", "text": bot_message})

    return render_template('index.html', messages=messages, next_options=next_options)


if __name__ == "__main__":
    app.run(debug=True)
