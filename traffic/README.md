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

    Epoch 1/10
    500/500 [==============================] - 12s 21ms/step - loss: 5.4718 - accuracy: 0.0521
    Epoch 2/10
    500/500 [==============================] - 9s 19ms/step - loss: 3.5892 - accuracy: 0.0557
    Epoch 3/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.5422 - accuracy: 0.0534
    Epoch 4/10
    500/500 [==============================] - 10s 19ms/step - loss: 3.5199 - accuracy: 0.0559
    Epoch 5/10
    500/500 [==============================] - 9s 17ms/step - loss: 3.5098 - accuracy: 0.0546
    Epoch 6/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.5051 - accuracy: 0.0561
    Epoch 7/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.5028 - accuracy: 0.0547
    Epoch 8/10
    500/500 [==============================] - 8s 17ms/step - loss: 3.5016 - accuracy: 0.0569
    Epoch 9/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.5010 - accuracy: 0.0557
    Epoch 10/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.5007 - accuracy: 0.0569

    Changing droput to 0.3

    Epoch 1/10
    500/500 [==============================] - 11s 21ms/step - loss: 5.5375 - accuracy: 0.0626
    Epoch 2/10
    500/500 [==============================] - 10s 21ms/step - loss: 3.4120 - accuracy: 0.0932
    Epoch 3/10
    500/500 [==============================] - 10s 19ms/step - loss: 3.2764 - accuracy: 0.1303
    Epoch 4/10
    500/500 [==============================] - 8s 17ms/step - loss: 3.2097 - accuracy: 0.1406
    Epoch 5/10
    500/500 [==============================] - 9s 17ms/step - loss: 3.0428 - accuracy: 0.1850
    Epoch 6/10
    500/500 [==============================] - 9s 18ms/step - loss: 2.8801 - accuracy: 0.2130
    Epoch 7/10
    500/500 [==============================] - 10s 20ms/step - loss: 2.8191 - accuracy: 0.2222
    Epoch 8/10
    500/500 [==============================] - 9s 19ms/step - loss: 2.7294 - accuracy: 0.2396
    Epoch 9/10
    500/500 [==============================] - 9s 18ms/step - loss: 2.5964 - accuracy: 0.2738
    Epoch 10/10
    500/500 [==============================] - 9s 18ms/step - loss: 2.3795 - accuracy: 0.3365
        
    Dropout back to 0.5, nodes in hidden layer increased to 256

    Epoch 1/10
    500/500 [==============================] - 12s 22ms/step - loss: 5.4097 - accuracy: 0.0516
    Epoch 2/10
    500/500 [==============================] - 13s 26ms/step - loss: 3.5948 - accuracy: 0.0561
    Epoch 3/10
    500/500 [==============================] - 11s 22ms/step - loss: 3.5373 - accuracy: 0.0554
    Epoch 4/10
    500/500 [==============================] - 11s 22ms/step - loss: 3.5137 - accuracy: 0.0552
    Epoch 5/10
    500/500 [==============================] - 11s 22ms/step - loss: 3.5029 - accuracy: 0.0554
    Epoch 6/10
    500/500 [==============================] - 12s 23ms/step - loss: 3.4979 - accuracy: 0.0564
    Epoch 7/10
    500/500 [==============================] - 12s 25ms/step - loss: 3.4955 - accuracy: 0.0549
    Epoch 8/10
    500/500 [==============================] - 16s 33ms/step - loss: 3.4942 - accuracy: 0.0564
    Epoch 9/10
    500/500 [==============================] - 14s 29ms/step - loss: 3.4936 - accuracy: 0.0542
    Epoch 10/10
    500/500 [==============================] - 15s 29ms/step - loss: 3.4933 - accuracy: 0.0554

    nodes in hidden layer reduced to 64

    Epoch 1/10
    500/500 [==============================] - 8s 15ms/step - loss: 4.3928 - accuracy: 0.0544   
    Epoch 2/10
    500/500 [==============================] - 11s 22ms/step - loss: 3.5896 - accuracy: 0.0572
    Epoch 3/10
    500/500 [==============================] - 9s 19ms/step - loss: 3.5411 - accuracy: 0.0576
    Epoch 4/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.5186 - accuracy: 0.0576
    Epoch 5/10
    500/500 [==============================] - 8s 16ms/step - loss: 3.5081 - accuracy: 0.0571
    Epoch 6/10
    500/500 [==============================] - 9s 19ms/step - loss: 3.5032 - accuracy: 0.0576
    Epoch 7/10
    500/500 [==============================] - 9s 19ms/step - loss: 3.5008 - accuracy: 0.0576
    Epoch 8/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.4996 - accuracy: 0.0562
    Epoch 9/10
    500/500 [==============================] - 9s 18ms/step - loss: 3.4989 - accuracy: 0.0576
    Epoch 10/10
    500/500 [==============================] - 10s 19ms/step - loss: 3.4986 - accuracy: 0.0576

    nodes in hidden layer back to 128, increasing filters to 64

    Epoch 1/10
    500/500 [==============================] - 17s 33ms/step - loss: 5.4823 - accuracy: 0.0534
    Epoch 2/10
    500/500 [==============================] - 17s 34ms/step - loss: 3.5892 - accuracy: 0.0559
    Epoch 3/10
    500/500 [==============================] - 16s 31ms/step - loss: 3.5399 - accuracy: 0.0559
    Epoch 4/10
    500/500 [==============================] - 16s 33ms/step - loss: 3.5165 - accuracy: 0.0559
    Epoch 5/10
    500/500 [==============================] - 15s 30ms/step - loss: 3.5057 - accuracy: 0.0559
    Epoch 6/10
    500/500 [==============================] - 16s 31ms/step - loss: 3.5006 - accuracy: 0.0559
    Epoch 7/10
    500/500 [==============================] - 15s 31ms/step - loss: 3.4982 - accuracy: 0.0559
    Epoch 8/10
    500/500 [==============================] - 16s 33ms/step - loss: 3.4970 - accuracy: 0.0559
    Epoch 9/10
    500/500 [==============================] - 16s 32ms/step - loss: 3.4964 - accuracy: 0.0559
    Epoch 10/10
    500/500 [==============================] - 19s 37ms/step - loss: 3.4960 - accuracy: 0.0559

    16 filters:

    Epoch 1/10
    500/500 [==============================] - 7s 12ms/step - loss: 5.3087 - accuracy: 0.0524   
    Epoch 2/10
    500/500 [==============================] - 6s 12ms/step - loss: 3.5908 - accuracy: 0.0541
    Epoch 3/10
    500/500 [==============================] - 6s 12ms/step - loss: 3.5428 - accuracy: 0.0537
    Epoch 4/10
    500/500 [==============================] - 6s 13ms/step - loss: 3.5208 - accuracy: 0.0542
    Epoch 5/10
    500/500 [==============================] - 6s 13ms/step - loss: 3.5107 - accuracy: 0.0559
    Epoch 6/10
    500/500 [==============================] - 6s 13ms/step - loss: 3.5064 - accuracy: 0.0552
    Epoch 7/10
    500/500 [==============================] - 6s 13ms/step - loss: 3.5037 - accuracy: 0.0549
    Epoch 8/10
    500/500 [==============================] - 7s 13ms/step - loss: 3.5026 - accuracy: 0.0546
    Epoch 9/10
    500/500 [==============================] - 7s 13ms/step - loss: 3.5020 - accuracy: 0.0554
    Epoch 10/10
    500/500 [==============================] - 7s 13ms/step - loss: 3.5018 - accuracy: 0.0547
    333/333 - 1s - loss: 3.4931 - accuracy: 0.0570 - 1s/epoch - 4ms/step

    filters back to 32, pool size: (3,3)

    Epoch 1/10
    500/500 [==============================] - 8s 14ms/step - loss: 4.4413 - accuracy: 0.0594   
    Epoch 2/10
    500/500 [==============================] - 8s 15ms/step - loss: 3.5745 - accuracy: 0.0648
    Epoch 3/10
    500/500 [==============================] - 8s 16ms/step - loss: 3.3154 - accuracy: 0.1349
    Epoch 4/10
    500/500 [==============================] - 7s 14ms/step - loss: 2.9036 - accuracy: 0.2173
    Epoch 5/10
    500/500 [==============================] - 7s 13ms/step - loss: 2.4351 - accuracy: 0.3185
    Epoch 6/10
    500/500 [==============================] - 7s 13ms/step - loss: 2.0311 - accuracy: 0.3967
    Epoch 7/10
    500/500 [==============================] - 7s 14ms/step - loss: 1.7785 - accuracy: 0.4664
    Epoch 8/10
    500/500 [==============================] - 7s 14ms/step - loss: 1.6108 - accuracy: 0.5038
    Epoch 9/10
    500/500 [==============================] - 7s 14ms/step - loss: 1.4889 - accuracy: 0.5424
    Epoch 10/10
    500/500 [==============================] - 7s 14ms/step - loss: 1.3577 - accuracy: 0.5820
    333/333 - 2s - loss: 0.7372 - accuracy: 0.7512 - 2s/epoch - 5ms/step

    Pool size: (4,4)

    Epoch 1/10
    500/500 [==============================] - 7s 13ms/step - loss: 5.0176 - accuracy: 0.0511   
    Epoch 2/10
    500/500 [==============================] - 6s 12ms/step - loss: 3.5891 - accuracy: 0.0532
    Epoch 3/10
    500/500 [==============================] - 8s 15ms/step - loss: 3.5398 - accuracy: 0.0563
    Epoch 4/10
    500/500 [==============================] - 7s 13ms/step - loss: 3.5171 - accuracy: 0.0552
    Epoch 5/10
    500/500 [==============================] - 6s 13ms/step - loss: 3.5070 - accuracy: 0.0563
    Epoch 6/10
    500/500 [==============================] - 6s 13ms/step - loss: 3.5015 - accuracy: 0.0572
    Epoch 7/10
    500/500 [==============================] - 7s 13ms/step - loss: 3.4990 - accuracy: 0.0572
    Epoch 8/10
    500/500 [==============================] - 7s 13ms/step - loss: 3.4978 - accuracy: 0.0573
    Epoch 9/10
    500/500 [==============================] - 7s 14ms/step - loss: 3.4972 - accuracy: 0.0569
    Epoch 10/10
    500/500 [==============================] - 7s 14ms/step - loss: 3.5052 - accuracy: 0.0575
    333/333 - 2s - loss: 3.4997 - accuracy: 0.0549 - 2s/epoch - 5ms/step

    Pool size back to (3,3), activation of hidden layer: sigmoid