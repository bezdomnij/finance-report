from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw
from util import util
import logging


def get_df(f):
	df = pd.DataFrame()
	try:
		df = pd.read_csv(f, encoding='utf-16', sep='\t', header=0, index_col=None)
	except Exception as e:
		print(f"mar konvertaltuk..., error: {e}")
		df = pd.read_csv(f, sep='\t', header=0, index_col=None)
	finally:
		return df


def google_audio(finrep_dir, table='stg_fin2_20012_google_audio', hova='19'):
	files = []
	df = pd.DataFrame()
	src = Path(finrep_dir).joinpath('google_audio')
	for f in src.iterdir():
		if f.suffix == '':
			continue
		ftype, period = util.check_incoming(f)
		if ftype == 'ga':
			files.append(f)
	for f in files:
		df = get_df(f)
		if df.shape[0] > 0:
			print(f.name, df['Earnings Amount'].astype(float).sum())

	# finds the latest and write that one to sql
	if len(files) > 1:
		period_file = {}
		for f in files:
			name_parts = f.stem.split('_')
			period = tuple(name_parts[-1].split('-'))
			period_file[period[0] * 100 + period[1]] = f
		the_one = period_file[sorted(period_file.keys())[-1]]
		df = get_df(the_one)
	elif len(files) == 1:
		df = get_df(files[0])
	else:
		print("No Google file there...")
		return
	print(df.info)
	sqw.write_to_db(df, table, action='replace', hova=hova)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
	google_audio('/Users/frank/pd/finance_report', hova='19')
	# google_audio('h:/NextCloud/Finance/szamitas/2021_11_november')
