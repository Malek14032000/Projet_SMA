#### Efficiency / Performance Metrics
# Total waste disposed through time
# Time taken to dispose of all waste
# Total green waste moved through time (or just the time when the green zone is empty)
# Total yellow waste moved through time (or just the time when the yellow zone is empty)
# Total red waste moved through time (or just the time when the red zone is empty)
# Time spent not performing useful work

#### Resource / Load Distribution
# Waste handled per agent
# Distance traveled per agent
# Gini coef of work (Low: tasks fairly distributed. High: inefficiencies / overworked agents.)

#### Robustness
# Variance across multiple simulation runs

from objects import WasteDisposalZone, Waste




# Total waste disposed through time
def compute_disposed_waste(model):
    agents = model.agents
    n_waste = len([w for w in agents if isinstance(w, Waste) and w.pos==(model.width-1, model.height//2)])
   
    if not hasattr(model, 'previous_n_waste'):
        model.previous_n_waste = 0
    
    total_waste = n_waste + model.previous_n_waste
    model.previous_n_waste += total_waste
    
    return total_waste

# Total waste left in the region through time
def transformed_waste_in_region(model, color):
    agents = model.agents
    n_waste = len([w for w in agents if isinstance(w, Waste) and w.radioactivity_level==color and w.pos==None])
    
    return n_waste



def compute_avg_time_not_working(model):
    pass

def compute_avg_distance_traveled(model):
    pass

def compute_gini_coef(model):
    pass

def compute_variance(model):
    pass
