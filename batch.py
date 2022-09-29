from datetime import datetime
import pandas as pd
from mesa.batchrunner import batch_run

from source.model import ForestFireResistance

params = {
    "density": [x/10 for x in range(0, 11, 1)],
    "width": 100,
    "height": 100,
    "intensity": range(1, 101, 10),
}

experiments_per_parameter_configuration = 100

max_steps_per_simulation = 100

results = batch_run(
    ForestFireResistance,
    parameters=params,
    iterations=experiments_per_parameter_configuration,
    max_steps=max_steps_per_simulation,
    data_collection_period=-1,
    display_progress=True,
)

results_df = pd.DataFrame(results)

print(results_df)

now = str(datetime.now()).replace(" : ", " -").replace(" ", " -")

file_name_suffix = (
    " _iter_ "
    + str(experiments_per_parameter_configuration)
    + " _steps_ "
    + str(max_steps_per_simulation)
    + " _ "
    + now
)

model_name_preffix = "ForestFireResistance"

file_name = model_name_preffix + "_model_data" + file_name_suffix + ".csv"

results_df.to_csv('output/' + file_name)
