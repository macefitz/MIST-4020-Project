from flask import Flask, flash, render_template, redirect, url_for, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again', 'error')
    return render_template('login.html')

@app.route('/register', methods =['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

class CPU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    sockettype = db.Column(db.String(50))
    price = db.Column(db.String(10))
    wattage = db.Column(db.Integer)

class GPU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    price = db.Column(db.String(10))
    wattage = db.Column(db.Integer)

class CPU_Cooler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    price = db.Column(db.String(10))
    wattage = db.Column(db.Integer)

class RAM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    memorytype = db.Column(db.String(10))
    price = db.Column(db.String(10))
    wattage = db.Column(db.Integer)

class Motherboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    sockettype = db.Column(db.String(50))
    memorytype = db.Column(db.String(10))
    price = db.Column(db.String(10))
    wattage = db.Column(db.Integer)

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    price = db.Column(db.String(10))
    wattage = db.Column(db.Integer)

class PC_Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    price = db.Column(db.String(10))

class Power_Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    price = db.Column(db.String(10))
    wattage = db.Column(db.Integer)

def create_tables():
    with app.app_context():
        db.create_all()
        
        # CPU data
        cpu_data = [
            {'brand': 'AMD', 'model': 'RYZEN 7 7800X3D', 'price': '$369.00', 'wattage': 162, 'socket': 'AM4'},
            {'brand': 'AMD', 'model': 'RYZEN 7 7600X', 'price': '$229.00', 'wattage': 105, 'socket': 'AM4'},
            {'brand': 'Intel', 'model': 'i9-12900K', 'price': '$599.00', 'wattage': 125, 'socket': 'LGA1700'},
            {'brand': 'Intel', 'model': 'i7-12700K', 'price': '$399.00', 'wattage': 125, 'socket': 'LGA1700'},
        ]

        for cpu_info in cpu_data:
            cpu = CPU(brand=cpu_info['brand'], model=cpu_info['model'], price=cpu_info['price'], wattage=cpu_info['wattage'], sockettype=cpu_info['socket'])
            db.session.add(cpu)
        
        # GPU data
        gpu_data = [
            {'brand': 'Nvidia', 'model': 'RTX 3080', 'price': '$799.00', 'wattage': 320},
            {'brand': 'AMD', 'model': 'RX 6800 XT', 'price': '$649.00', 'wattage': 300},
            {'brand': 'Nvidia', 'model': 'RTX 3090', 'price': '$1499.00', 'wattage': 350},
            {'brand': 'AMD', 'model': 'RX 6900 XT', 'price': '$999.00', 'wattage': 330}
        ]
        for gpu_info in gpu_data:
            gpu = GPU(brand=gpu_info['brand'], model=gpu_info['model'], price=gpu_info['price'], wattage=gpu_info['wattage'])
            db.session.add(gpu)
        
        # CPU Cooler data
        cpu_cooler_data = [
            {'brand': 'Cooler Master', 'model': 'Hyper 212 RGB', 'price': '$39.99', 'wattage': 150},
            {'brand': 'Noctua', 'model': 'NH-D15', 'price': '$89.95', 'wattage': 140},
            {'brand': 'Corsair', 'model': 'H100i RGB Platinum', 'price': '$159.99', 'wattage': 75},
            {'brand': 'NZXT', 'model': 'Kraken X63', 'price': '$149.99', 'wattage': 30}
        ]
        for cooler_info in cpu_cooler_data:
            cooler = CPU_Cooler(brand=cooler_info['brand'], model=cooler_info['model'], price=cooler_info['price'], wattage=cooler_info['wattage'])
            db.session.add(cooler)
        
        # RAM data
        ram_data = [
            {'brand': 'Corsair', 'model': 'Vengeance RGB Pro', 'price': '$79.99', 'wattage': 5, 'memory_type': 'DDR4'},
            {'brand': 'G.Skill', 'model': 'Trident Z RGB', 'price': '$89.99', 'wattage': 5, 'memory_type': 'DDR5'},
            {'brand': 'Crucial', 'model': 'Ballistix RGB', 'price': '$69.99', 'wattage': 5, 'memory_type': 'DDR4'},
            {'brand': 'Kingston', 'model': 'HyperX Fury RGB', 'price': '$74.99', 'wattage': 5, 'memory_type': 'DDR4'}
        ]
        for ram_info in ram_data:
            ram = RAM(brand=ram_info['brand'], model=ram_info['model'], price=ram_info['price'], wattage=ram_info['wattage'])
            db.session.add(ram)
        
        # Motherboard data
        motherboard_data = [
            {'brand': 'Asus', 'model': 'ROG Strix X570-E', 'price': '$299.99', 'wattage': 10, 'socket': 'AM4', 'memory_type': 'DDR4'},
            {'brand': 'Gigabyte', 'model': 'Aorus Elite X570', 'price': '$199.99', 'wattage': 10, 'socket': 'AM4', 'memory_type': 'DDR4'},
            {'brand': 'Asus', 'model': 'ROG Strix Z690-E', 'price': '$349.99', 'wattage': 10, 'socket': 'LGA1700', 'memory_type': 'DDR5'},
            {'brand': 'Gigabyte', 'model': 'Aorus Pro Z690', 'price': '$289.99', 'wattage': 10, 'socket': 'LGA1700', 'memory_type': 'DDR5'}
        ]

        for mobo_info in motherboard_data:
            mobo = Motherboard(brand=mobo_info['brand'], model=mobo_info['model'], price=mobo_info['price'], wattage=mobo_info['wattage'], sockettype=mobo_info['socket'])
            db.session.add(mobo)
        
        # Storage data
        storage_data = [
            {'brand': 'Samsung', 'model': '970 EVO Plus', 'price': '$129.99', 'wattage': 5},
            {'brand': 'WD', 'model': 'Black SN750', 'price': '$99.99', 'wattage': 5},
            {'brand': 'Crucial', 'model': 'MX500', 'price': '$79.99', 'wattage': 5},
            {'brand': 'Seagate', 'model': 'FireCuda 510', 'price': '$149.99', 'wattage': 5}
        ]
        for storage_info in storage_data:
            storage = Storage(brand=storage_info['brand'], model=storage_info['model'], price=storage_info['price'], wattage=storage_info['wattage'])
            db.session.add(storage)
        
        # PC Case data
        pc_case_data = [
            {'brand': 'NZXT', 'model': 'H510', 'price': '$69.99'},
            {'brand': 'Fractal Design', 'model': 'Meshify C', 'price': '$99.99'},
            {'brand': 'Corsair', 'model': 'Crystal 570X RGB', 'price': '$179.99'},
            {'brand': 'Cooler Master', 'model': 'MasterBox TD500 Mesh', 'price': '$99.99'}
        ]
        for case_info in pc_case_data:
            case = PC_Case(brand=case_info['brand'], model=case_info['model'], price=case_info['price'])
            db.session.add(case)
        
        # Power Supply data
        power_supply_data = [
            {'brand': 'EVGA', 'model': 'SuperNOVA 650 G5', 'price': '$89.99', 'wattage': 650},
            {'brand': 'Corsair', 'model': 'RM750x', 'price': '$119.99', 'wattage': 750},
            {'brand': 'Seasonic', 'model': 'Focus GX-850', 'price': '$139.99', 'wattage': 850},
            {'brand': 'Thermaltake', 'model': 'Toughpower Grand RGB 850W', 'price': '$129.99', 'wattage': 850}
        ]
        for psu_info in power_supply_data:
            psu = Power_Supply(brand=psu_info['brand'], model=psu_info['model'], price=psu_info['price'], wattage=psu_info['wattage'])
            db.session.add(psu)
        
        db.session.commit()

def calculate_total_cost(selected_components):
    total_cost = 0
    for component in selected_components:
        if component:
            total_cost += float(component.price.strip('$'))
    return total_cost


@app.route('/')
def home():
    if current_user.is_authenticated:
        cpus = CPU.query.all()
        gpus = GPU.query.all()
        cpu_coolers = CPU_Cooler.query.all()
        rams = RAM.query.all()
        motherboards = Motherboard.query.all()
        storages = Storage.query.all()
        pc_cases = PC_Case.query.all()
        power_supplies = Power_Supply.query.all()

        return render_template("home.html", cpus=cpus, gpus=gpus, cpu_coolers=cpu_coolers, rams=rams, motherboards=motherboards, storages=storages, pc_cases=pc_cases, power_supplies=power_supplies)
    else:
        return redirect(url_for('login'))

@app.route('/build-pc', methods=['POST'])
def build_pc():
    cpu_id = request.form['cpu']
    cpu_cooler_id = request.form['cpu_cooler']
    gpu_id = request.form['gpu']
    motherboard_id = request.form['motherboard']
    ram_id = request.form['ram']
    storage_id = request.form['storage']
    power_supply_id = request.form['power_supply']
    pc_case_id = request.form['pc_case']

    # Query selected components by ID
    cpu = CPU.query.get(cpu_id)
    cpu_cooler = CPU_Cooler.query.get(cpu_cooler_id)
    gpu = GPU.query.get(gpu_id)
    motherboard = Motherboard.query.get(motherboard_id)
    ram = RAM.query.get(ram_id)
    storage = Storage.query.get(storage_id)
    power_supply = Power_Supply.query.get(power_supply_id)
    pc_case = PC_Case.query.get(pc_case_id)
     # Calculate total wattage excluding power supply
    total_wattage = cpu.wattage + cpu_cooler.wattage + gpu.wattage + motherboard.wattage + ram.wattage + storage.wattage

    # Calculate total price
    total_price = float(cpu.price.strip('$')) + float(cpu_cooler.price.strip('$')) + float(gpu.price.strip('$')) + float(motherboard.price.strip('$')) + float(ram.price.strip('$')) + float(storage.price.strip('$')) + float(pc_case.price.strip('$')) + float(power_supply.price.strip('$'))

    cpu_socket = cpu.sockettype
    motherboard_socket = motherboard.sockettype
    # Render build summary template and pass form data
    return render_template('build-pc.html', cpu=cpu, cpu_cooler=cpu_cooler,
                       gpu=gpu, motherboard=motherboard, ram=ram,
                       storage=storage, power_supply=power_supply,
                       pc_case=pc_case, total_price=total_price,
                       total_wattage=total_wattage)

@app.route('/download_receipt', methods=['POST'])
def download_receipt():
    # Get selected component IDs from the form
    cpu_id = request.form['cpu']
    cpu_cooler_id = request.form['cpu_cooler']
    gpu_id = request.form['gpu']
    motherboard_id = request.form['motherboard']
    ram_id = request.form['ram']
    storage_id = request.form['storage']
    power_supply_id = request.form['power_supply']
    pc_case_id = request.form['pc_case']

    # Query selected components by ID
    cpu = CPU.query.get(cpu_id)
    cpu_cooler = CPU_Cooler.query.get(cpu_cooler_id)
    gpu = GPU.query.get(gpu_id)
    motherboard = Motherboard.query.get(motherboard_id)
    ram = RAM.query.get(ram_id)
    storage = Storage.query.get(storage_id)
    power_supply = Power_Supply.query.get(power_supply_id)
    pc_case = PC_Case.query.get(pc_case_id)

    # Calculate total wattage and total cost
    total_wattage = cpu.wattage + cpu_cooler.wattage + gpu.wattage + motherboard.wattage + ram.wattage + storage.wattage
    total_price = calculate_total_cost([cpu, cpu_cooler, gpu, motherboard, ram, storage, pc_case, power_supply])

    # Generate receipt content
    receipt_content = generate_receipt_content(cpu, cpu_cooler, gpu, motherboard, ram, storage, power_supply, pc_case, total_wattage, total_price)

    # Create a response with the receipt content as a text file
    response = make_response(receipt_content)
    response.headers['Content-Disposition'] = 'attachment; filename=pc_receipt.txt'
    response.headers['Content-type'] = 'text/plain'

    return response

def generate_receipt_content(cpu, cpu_cooler, gpu, motherboard, ram, storage, power_supply, pc_case, total_wattage, total_price):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    receipt_content = f"""
    ======================================
               Micro Center
          PC Build Receipt
    --------------------------------------
    Date:         {current_datetime}
    CPU:          {cpu.brand} - {cpu.model}
    CPU Cooler:   {cpu_cooler.brand} - {cpu_cooler.model}
    GPU:          {gpu.brand} - {gpu.model}
    Motherboard:  {motherboard.brand} - {motherboard.model}
    RAM:          {ram.brand} - {ram.model}
    Storage:      {storage.brand} - {storage.model}
    Power Supply: {power_supply.brand} - {power_supply.model}
    PC Case:      {pc_case.brand} - {pc_case.model}
    --------------------------------------
    Total Wattage: {total_wattage} W
    Total Price:   ${total_price}
    --------------------------------------
    About Micro Center:
    Micro Center is a leading retailer of computer products and electronics. With over 25 locations nationwide,
    Micro Center offers a vast selection of computer hardware, software, and accessories at competitive prices.
    Contact Information:
    Phone: 1-800-234-4343
    Email: info@microcenter.com
    Website: www.microcenter.com
    Visit us in-store or online for all your technology needs!
    ======================================
    """
    return receipt_content
if __name__ == "__main__":
    create_tables()  
    app.run(host="0.0.0.0", port=8000)