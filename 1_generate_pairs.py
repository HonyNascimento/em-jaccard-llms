import pandas as pd
import os
import random

def load_raw_data_walmart(records_path, dpl_path, ndpl_path):
    records = pd.read_csv(records_path, sep='\t', encoding='utf-8')
    dpl = pd.read_csv(dpl_path, sep='\t', encoding='utf-8')
    ndpl = pd.read_csv(ndpl_path, sep='\t', encoding='utf-8')
    records.fillna('', inplace=True)

    records['id'] = records['id'].astype(str)
    dpl['id1'] = dpl['id1'].astype(str)
    dpl['id2'] = dpl['id2'].astype(str)
    ndpl['id1'] = ndpl['id1'].astype(str)
    ndpl['id2'] = ndpl['id2'].astype(str)

    return records, dpl, ndpl


def build_pairs_walmart(records, pairs_df, is_match):
    left = pairs_df.merge(records, left_on='id1', right_on='id', suffixes=('', '_left'))
    right = pairs_df.merge(records, left_on='id2', right_on='id', suffixes=('', '_right'))
    merged = left.merge(right, on=['id1', 'id2'])
    merged['is_match'] = is_match
    return merged


def load_raw_data_abt(abt_path, buy_path, mapping_path):
    abt = pd.read_csv(abt_path, encoding='ISO-8859-1')
    buy = pd.read_csv(buy_path, encoding='ISO-8859-1')
    matches = pd.read_csv(mapping_path, encoding='ISO-8859-1')

    abt.rename(columns={'id': 'id_abt'}, inplace=True)
    buy.rename(columns={'id': 'id_buy'}, inplace=True)
    abt.fillna('', inplace=True)
    buy.fillna('', inplace=True)
    return abt, buy, matches


def create_positive_pairs_abt(abt, buy, matches):
    positives = matches.merge(abt, left_on='idAbt', right_on='id_abt') \
                      .merge(buy, left_on='idBuy', right_on='id_buy', suffixes=('_abt', '_buy'))
    positives['is_match'] = 1
    return positives


def create_negative_pairs_abt(abt, buy, matches, n_negatives):
    abt_ids = abt['id_abt'].tolist()
    buy_ids = buy['id_buy'].tolist()
    match_set = set(zip(matches['idAbt'], matches['idBuy']))

    non_matches = set()
    while len(non_matches) < n_negatives:
        a = random.choice(abt_ids)
        b = random.choice(buy_ids)
        if (a, b) not in match_set:
            non_matches.add((a, b))
            match_set.add((a, b))

    non_matches_df = pd.DataFrame(list(non_matches), columns=['idAbt', 'idBuy'])
    non_matches_df = non_matches_df.merge(abt, left_on='idAbt', right_on='id_abt') \
                                     .merge(buy, left_on='idBuy', right_on='id_buy', suffixes=('_abt', '_buy'))
    non_matches_df['is_match'] = 0
    return non_matches_df


def combine_and_save(positives, negatives, output_path):
    full_df = pd.concat([positives, negatives], ignore_index=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    full_df.to_csv(output_path, index=False)
    print(f"Dataset salvo em: {output_path}")


def main():
    random.seed(42)

    # Walmart-Amazon
    records_path = 'data/Walmart-Amazon/amazon_walmart.tsv'
    dpl_path = 'data/Walmart-Amazon/amazon_walmart_DPL.tsv'
    ndpl_path = 'data/Walmart-Amazon/amazon_walmart_NDPL.tsv'
    output_path_walmart = 'data/walmart_amazon_pairs_labeled.csv'

    records, dpl, ndpl = load_raw_data_walmart(records_path, dpl_path, ndpl_path)
    positives = build_pairs_walmart(records, dpl, is_match=1)
    negatives = build_pairs_walmart(records, ndpl, is_match=0)
    combine_and_save(positives, negatives, output_path_walmart)

    # Abt-Buy
    abt_path = 'data/Abt-Buy/Abt.csv'
    buy_path = 'data/Abt-Buy/Buy.csv'
    mapping_path = 'data/Abt-Buy/abt_buy_perfectMapping.csv'
    output_path_abt = 'data/abt_buy_pairs_labeled.csv'

    abt, buy, matches = load_raw_data_abt(abt_path, buy_path, mapping_path)
    positives_abt = create_positive_pairs_abt(abt, buy, matches)
    negatives_abt = create_negative_pairs_abt(abt, buy, matches, n_negatives=len(positives_abt))
    combine_and_save(positives_abt, negatives_abt, output_path_abt)


if __name__ == '__main__':
    main()
