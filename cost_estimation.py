import pandas as pd

# ✅ Create and save df_parts.csv
def create_parts_csv():
    data = {
        "Part Name": ["Hydraulic Cylinder Spacer"],
        "Part Number": ["3100130381"]
    }
    df_parts = pd.DataFrame(data)
    df_parts.to_csv("df_parts.csv", index=False)
    print("✅ df_parts.csv created successfully!")

# ✅ Create and save df_process.csv
def create_process_csv():
    data = {
        "Process": ["Milling all side, drill Dia12", "Grinding"]
    }
    df_process = pd.DataFrame(data)
    df_process.to_csv("df_process.csv", index=False)
    print("✅ df_process.csv created successfully!")

# ✅ Create and save df_machine.csv
def create_machine_csv():
    data = {
        "Machine": ["VMC", "Slide Grinding"],
        "Setup Time (mins)": [20, 30],
        "Cycle Time (mins)": [30, 15],
        "Machine Hour Rate (INR)": [450, 600]
    }
    
    # Calculate machine cost as Cycle Time × Hourly Rate ÷ 60
    df_machine = pd.DataFrame(data)
    df_machine["Cost (INR)"] = (df_machine["Cycle Time (mins)"] * df_machine["Machine Hour Rate (INR)"]) / 60
    df_machine.to_csv("df_machine.csv", index=False)
    
    print("✅ df_machine.csv created successfully with machine costs!")

# ✅ Function to calculate the machine cost
def calculate_machine_cost():
    # Load machine data
    df_machine = pd.read_csv("df_machine.csv")
    
    # Sum the "Cost (INR)" column
    machine_cost = df_machine["Cost (INR)"].sum()
    
    print(f"🔧 Machine Cost: {machine_cost:.2f} INR")
    return machine_cost

# ✅ Calculate total cost estimation including machine cost
def calculate_total_cost(material_cost, margin=20, packing=50, negotiation_margin=5, transportation=100):
    # Calculate machine cost
    machine_cost = calculate_machine_cost()
    
    # Margin calculation
    margin_cost = material_cost * (margin / 100)
    
    # Negotiation Margin
    negotiation_cost = material_cost * (negotiation_margin / 100)
    
    # Total estimated cost calculation
    total_cost = material_cost + machine_cost + margin_cost + packing + negotiation_cost + transportation
    
    print("\n💡 Cost Estimation Details:")
    print(f"Material Cost: {material_cost} INR")
    print(f"Machine Cost: {machine_cost:.2f} INR")
    print(f"Margin (20%): {margin_cost:.2f} INR")
    print(f"Packing: {packing} INR")
    print(f"Negotiation Margin (5%): {negotiation_cost:.2f} INR")
    print(f"Transportation: {transportation} INR")
    print(f"✅ Total Estimated Cost: {total_cost:.2f} INR")
    
    return total_cost

# ✅ Main execution
create_parts_csv()
create_process_csv()
create_machine_csv()

# Example cost estimation
material_cost = 750  # INR (example material cost)
total_estimated_cost = calculate_total_cost(material_cost)
