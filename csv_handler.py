import pandas as pd
import os

def append_to_csv(rows, file_path):
    new_df = pd.DataFrame(rows)

    # Remove duplicates within generated batch
    new_df = new_df.drop_duplicates()

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)

        combined_df = pd.concat([existing_df, new_df])

        # Remove duplicates against existing CSV
        combined_df = combined_df.drop_duplicates()

        combined_df.to_csv(file_path, index=False)

    else:
        new_df.to_csv(file_path, index=False)