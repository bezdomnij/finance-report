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
	src = Path(finrep_dir).joinpath('google_audio')
	for f in src.iterdir():
		if f.suffix == '':
			continue
		ftype, period = util.check_google_file_name(f.name)
		if ftype == 'ga':
			files.append(f)
	for f in files:
		df = get_df(f)
		if df.shape[0] > 0:
			print(f"{f.name}, SUM: {df['Earnings Amount'].astype(float).sum():.2f}")

	# finds the latest and write that one to sql
	if len(files) > 1:
		period_file = {}
		for f in files:
			name_parts = f.stem.split('_')
			period = tuple(name_parts[-1].split('-'))
			f_key = int(period[0]) * 100 + int(period[1])
			# print(f_key)
			period_file[f_key] = f
		the_one_to_write = period_file[sorted(period_file.keys())[-1]]
		df = get_df(the_one_to_write)
	elif len(files) == 1:
		df = get_df(files[0])
	else:
		print("No writeable Google file there...")
		return


# print(df.info)
# sqw.write_to_db(df, table, action='replace', hova=hova)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w', format='%(asctime)s %(message)s')
	google_audio('/Users/frank/pd/finance_report', hova='19')
# google_audio('h:/NextCloud/Finance/szamitas/2021_11_november')
