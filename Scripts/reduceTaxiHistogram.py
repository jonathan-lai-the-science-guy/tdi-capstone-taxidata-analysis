import pandas as pd

histResult = pd.read_hdf('histResult.hdf','table')
histResult['hour'] = histResult.index
histResult.reset_index(drop=True, inplace=True)
z = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 22: -2, 23: -1}
histResult['hour'] = histResult['hour'].map(z)
times = {0: '12 - 1AM', 1: '1 - 2AM', 2: '2 - 3AM', 3: '3 - 4AM', 4: '4 - 5AM', 22: '10PM - 11PM', 23: '11PM - 12AM'}
histResult['times'] = histResult['hour'].map(times)
tmp = histResult.groupby('hour').sum()
tmp.to_hdf('reducedHistResult.hdf','table')
