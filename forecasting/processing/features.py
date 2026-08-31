from config import settings

def create_x_and_y(master):
    target_col = settings["target"]["column"]
    split_fraction = settings["split"]["train_fraction"]

    feature_col = [c for c in master.columns if c not in ["date", target_col]]

    split_idx = int(len(master) * split_fraction)

    train = master.iloc[:split_idx]
    test = master.iloc[split_idx:]

    x_train = train[feature_col]
    x_test = test[feature_col]
    y_train = train[target_col]
    y_test = test[target_col]

    return x_train, x_test, y_train, y_test