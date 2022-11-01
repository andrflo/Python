# Visualization of large data sets of oil analyses
    #### Video Demo:  <https://1drv.ms/v/s!Ah49GwRcwWoNgYEXFxP2Rq8LWOsXjQ?e=jD1MFe>
    #### Description attempts:
    model = tf.keras.models.Sequential([

        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Add an output layer with NUM_CATEGORIES output units
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
    Epoch 1/10
    500/500 [==============================] - 9s 17ms/step - loss: 3.7011 - accuracy: 0.1212  
    Epoch 2/10
    500/500 [==============================] - 9s 17ms/step - loss: 2.7567 - accuracy: 0.2262
    Epoch 3/10
    500/500 [==============================] - 9s 17ms/step - loss: 2.4845 - accuracy: 0.2830
    Epoch 4/10
    500/500 [==============================] - 10s 21ms/step - loss: 2.3256 - accuracy: 0.3134
    Epoch 5/10
    500/500 [==============================] - 9s 18ms/step - loss: 2.1759 - accuracy: 0.3412
    Epoch 6/10
    500/500 [==============================] - 9s 18ms/step - loss: 2.0683 - accuracy: 0.3662
    Epoch 7/10
    500/500 [==============================] - 8s 16ms/step - loss: 1.9511 - accuracy: 0.3905
    Epoch 8/10
    500/500 [==============================] - 10s 20ms/step - loss: 1.8637 - accuracy: 0.4147
    Epoch 9/10
    500/500 [==============================] - 10s 19ms/step - loss: 1.8070 - accuracy: 0.4289
    Epoch 10/10
    500/500 [==============================] - 8s 17ms/step - loss: 1.7356 - accuracy: 0.4489
    333/333 - 2s - loss: 1.0477 - accuracy: 0.6585 - 2s/epoch - 5ms/step

    Changing droput to 0.8
    



