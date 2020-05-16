import matplotlib
from jedi.api.refactoring import inline
from matplotlib import pyplot as plt
import OpenBlender
import pandas as pd
import json

action = 'API_getObservationsFromDataset'
parameters = {
 'token':'5ebfc19495162901b0611bd8umq4MIjT5rvl9pb4TDdYbPXT187wWZ',
 'id_dataset':'5e7a0d5d9516296cb86c6263',
 'date_filter':{
               "start_date":"2020-01-01T06:00:00.000Z",
               "end_date":"2020-03-11T06:00:00.000Z"},
 'consumption_confirmation':'on',
 'add_date' : 'date'
}

df_confirmed = pd.read_json(json.dumps(OpenBlender.call(action, parameters)['sample']), convert_dates=False, convert_axes=False).sort_values('timestamp', ascending=False)
df_confirmed.reset_index(drop=True, inplace=True)
df_confirmed.head(10)
