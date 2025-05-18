
import tensorflow as tf, numpy as np, os
from util.constants import MID_SEGMENT

def build_model(input_dim=39):
    inputs=tf.keras.Input(shape=(input_dim,))
    x=tf.keras.layers.Dense(64, activation='relu')(inputs)
    # Mid‑Boost：對輸入 21‑30 範圍做權重放大，這裡用乘法層示意
    boost_mask=np.array([1.3 if (i+1) in MID_SEGMENT else 1.0 for i in range(input_dim)], dtype='float32')
    boosted=tf.keras.layers.Multiply()([inputs, boost_mask])
    x2=tf.keras.layers.Dense(64, activation='relu')(boosted)
    concat=tf.keras.layers.Concatenate()([x,x2])
    outputs=tf.keras.layers.Dense(1, activation='sigmoid')(concat)
    model=tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

def load_or_train(model_path, X, y, epochs=3):
    if os.path.exists(model_path):
        model=tf.keras.models.load_model(model_path)
    else:
        model=build_model(X.shape[1])
        model.fit(X, y, epochs=epochs, verbose=0)
        model.save(model_path)
    return model
