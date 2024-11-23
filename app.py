from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Hardcoded machine cost options for the dropdown
machine_options = {
    "Starter Kit 1 | 4 Cores | 16GB RAM | NVIDIA T4 16 GB VRAM": 0.99,
    "Starter Kit 2 | 4 Cores | 16GB RAM | NVIDIA A10 24 GB VRAM": 1.65,
    "Mid-tier 1 | 8 Cores | 32GB RAM | NVIDIA T4 16 GB VRAM": 1.99,
    "Mid-tier 2 | 8 Cores | 32GB RAM | NVIDIA A10 24 GB VRAM": 2.29,
    "High-end Studio 1 | 16 Cores | 64GB RAM | NVIDIA T4 16 GB VRAM": 2.99,
    "High-end Studio 2 | 16 Cores | 64GB RAM | NVIDIA A10 24 GB VRAM": 3.49,
    "Top-tier 1 | 32 Cores | 128GB RAM | NVIDIA T4 16 GB VRAM": 4.99,
    "Top-tier 2 | 64 Cores | 256GB RAM | NVIDIA T4 16 GB VRAM": 7.49,
    "Top-tier 3 | 32 Cores | 128GB RAM | NVIDIA A10 24 GB VRAM": 7.99,
    "Exceptional Power 1 | 48 Cores | 192GB RAM | 4 x NVIDIA T4 16 GB VRAM": 8.99,
    "Exceptional Power 3 | 64 Cores | 256GB RAM | NVIDIA A10 24 GB VRAM": 9.99,
    "Exceptional Power 2 | 96 Cores | 384GB RAM | 8 x NVIDIA T4 16 GB VRAM": 13.99,
    "Exceptional Power 4 | 48 Cores | 192GB RAM | 4 x NVIDIA A10 24 GB VRAM": 11.99,
    "Exceptional Power 5 | 96 Cores | 384GB RAM | 4 x NVIDIA A10 24 GB VRAM": 18.99,
    "Insanity | 192 Cores | 768GB RAM | 8 x NVIDIA A10 24 GB VRAM": 39.99
}

@app.route('/')
def index():
    # Set a default machine for the dropdown
    default_machine = "16 Cores | 64GB RAM   | NVIDIA A10 24 GB VRAM"
    return render_template('index.html', machine_options=machine_options, default_machine=default_machine)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Form inputs
    num_devs = int(request.form['num_devs'])
    on_prem_cost_per_dev = float(request.form['on_prem_cost_per_dev'])
    annual_maint_costs = float(request.form['annual_maint_costs'])
    usage_hours_per_year = int(request.form['usage_hours_per_year'])

    # Selected machine cost from the dropdown
    spark_prostation = request.form['spark_prostation']
    machine_cost_per_hour = machine_options[spark_prostation]

    # Check selected OS type
    os_type = request.form['os_type']
    if os_type == "linux":
        machine_cost_per_hour *= 0.75  # Apply 25% discount for Rocky Linux

    # Apply additional discount for high usage
    if usage_hours_per_year > 1000:
        machine_cost_per_hour *= 0.7  # Apply 30% discount

    # Cloud cost calculations
    cloud_cost_per_dev = machine_cost_per_hour * usage_hours_per_year
    total_cloud_cost = cloud_cost_per_dev * num_devs

    # On-prem cost calculations
    total_on_prem_cost = (on_prem_cost_per_dev * num_devs) + annual_maint_costs

    return jsonify({
        'cloud_cost': total_cloud_cost,
        'on_prem_cost': total_on_prem_cost
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
