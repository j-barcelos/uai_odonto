from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from models import db, Profissional, Paciente, Agendamento
from config import Config
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def home():
    professionals = Profissional.query.all()
    return render_template('index.html', professionals=professionals)

@app.route('/chat')
def chat_interface():
    return render_template('chat.html')

@app.route('/api/chat/message', methods=['POST'])
def process_chat_message():
    data = request.json
    user_input = data.get('message', '').lower().strip()
    current_step = data.get('current_step', 'greeting')
    
    response_text = "Olá! Sou o assistente virtual da Uai Odonto."
    action_taken = None
    new_step = current_step
    
    # Dicionário de serviços (aceita variações como "ortodontia" e "ortodoncia")
    services_dict = {
        'implantes': ['implant', 'implante'],
        'ortodontia': ['ortodontia', 'ortodoncia'],
        'harmonização': ['harmoniza', 'harmonização', 'estética'],
        'próteses': ['protese', 'prótese'],
        'endodontia': ['canal', 'endodontia']
    }
    
    # Verifica se o usuário mencionou algum serviço
    mentioned_service = None
    for service_name, keywords in services_dict.items():
        if any(keyword in user_input for keyword in keywords):
            mentioned_service = service_name
            break
    
    if current_step == 'greeting':
        if mentioned_service:
            response_text = f"Ótimo! Deseja agendar para **{mentioned_service.upper()}**?\nQual sua data preferida?"
            new_step = 'select_date'
            action_taken = {'service': mentioned_service}
            session['selected_service'] = mentioned_service
        elif any(w in user_input for w in ['olá', 'oi', 'sim', 'bom dia']):
            response_text = "Que bom te ver! Qual tratamento você procura?\nNossas especialidades: Implantes, Ortodontia, Harmonização, Próteses, Endodontia."
            new_step = 'select_service'
            action_taken = {'step': 'select_service'}
        else:
            response_text = "Olá! Como posso ajudar hoje? Podemos falar sobre tratamentos ou agendar sua consulta."
            new_step = 'greeting'
            
    elif current_step == 'select_service':
        if mentioned_service:
            response_text = f"Excelente escolha! Deseja agendar para **{mentioned_service.upper()}**?\nQual sua data preferida?"
            new_step = 'select_date'
            action_taken = {'service': mentioned_service}
            session['selected_service'] = mentioned_service
        else:
            response_text = "Desculpe, não entendi. Mencione um tratamento: Implantes, Ortodontia, Harmonização, etc."
            new_step = 'select_service'
            
    elif current_step == 'select_date':
        if mentioned_service:
            session['selected_service'] = mentioned_service
        response_text = "Perfeito! Agora me informe seu nome completo."
        new_step = 'get_name'
        
    elif current_step == 'get_name':
        words = user_input.split()
        if len(words) >= 2 and '@' not in user_input and sum(c.isdigit() for c in user_input) < 5:
            response_text = "Agora seu WhatsApp ou telefone."
            new_step = 'get_phone'
            action_taken = {'patient_name': user_input.title(), 'step': 'get_phone'}
        else:
            response_text = "Por favor, digite nome e sobrenome."
            new_step = 'get_name'
            
    elif current_step == 'get_phone':
        phone_only = ''.join(c for c in user_input if c.isdigit())
        if len(phone_only) >= 10:
            try:
                print(f"--- Iniciando salvamento para: {user_input.title()} ---")
                
                # Recupera o serviço escolhido da sessão
                service_name = session.pop('selected_service', 'Geral')
                print(f"Serviço recuperado: {service_name}")
                
                # 1. Criar Paciente
                new_patient = Paciente(
                    nome=user_input.title(),
                    email="cliente@temp.com",
                    telefone=phone_only
                )
                db.session.add(new_patient)
                db.session.flush()  # Pega o ID imediatamente
                print(f"Paciente criado com ID: {new_patient.paciente_id}")
                
                # 2. Calcular Data/Hora (Amanhã às 09:00 por padrão)
                target_date = datetime.utcnow().date() + timedelta(days=1)
                target_time = datetime.strptime("09:00", "%H:%M").time()
                print(f"Data: {target_date}, Hora: {target_time}")
                
                # 3. Criar AGENDAMENTO (isso é o que faltava!)
                new_appt = Agendamento(
                    paciente_id=new_patient.paciente_id,
                    data_consulta=target_date,
                    hora_consulta=target_time,
                    observacao=f"Agendamento via Chatbot para: {service_name}",
                    status='pendente'
                )
                db.session.add(new_appt)
                db.session.commit()
                print("✅ Agendamento salvo com sucesso!")
                
                response_text = f"✅ Agendamento confirmado!\nPaciente: {new_patient.nome}\nServiço: {service_name}\nData: {target_date.strftime('%d/%m')} às {target_time.strftime('%H:%M')}\n\nEntraremos em contato!"
                new_step = 'completed'
                action_taken = {'saved': True, 'patient_id': new_patient.paciente_id, 'appt_id': new_appt.agendamento_id}
                
            except Exception as e:
                db.session.rollback()
                error_msg = str(e)
                print(f"❌ ERRO AO SALVAR: {error_msg}")
                print(f"Tipo: {type(e).__name__}")
                response_text = f"⚠️ Erro ao salvar: {error_msg}. Tente novamente ou ligue: (11) 9999-8888"
                new_step = 'get_phone'
        else:
            response_text = "Telefone inválido. Digite com DDD (ex: 1199998888)."
            new_step = 'get_phone'
            action_taken = {'step': 'get_phone'}
    
    return jsonify({
        'response': response_text,
        'action': action_taken,
        'current_step': new_step
    })

@app.route('/admin')
def admin_dashboard():
    appointments = Agendamento.query.order_by(Agendamento.created_at.desc()).all()
    professionals = Profissional.query.all()
    patients = Paciente.query.all()
    return render_template('admin/dashboard.html', appointments=appointments, professionals=professionals, patients=patients)

@app.route('/admin/approve/<int:id>')
def approve_appointment(id):
    appt = Agendamento.query.get_or_404(id)
    appt.status = 'confirmado'
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Profissional.query.count() == 0:
            profissionais_iniciais = [
                Profissional(nome="Dr. Silva", especialidade="Implantes", telefone="(11) 9999-8888"),
                Profissional(nome="Dra. Santos", especialidade="Ortodontia", telefone="(11) 9999-7777"),
                Profissional(nome="Dr. Oliveira", especialidade="Endodontia", telefone="(11) 9999-6666"),
                Profissional(nome="Dra. Costa", especialidade="Harmonização", telefone="(11) 9999-5555")
            ]
            db.session.add_all(profissionais_iniciais)
            db.session.commit()
            print("✓ Profissionais iniciais criados!")
    
    print("\n🚀 Servidor iniciado!")
    print("   • Página: http://127.0.0.1:5000/")
    print("   • Chat:   http://127.0.0.1:5000/chat")
    print("   • Admin:  http://127.0.0.1:5000/admin")
    
    app.run(debug=True)
