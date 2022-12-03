# Experimentation Process

### Model No. 1

Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(128 neurons) + Dropout(0.5)

- **Result 1_1**: 2s - loss: 3.5036 - accuracy: 0.0530 - 2s/epoch - 6ms/step
- **Result 1_2**: 2s - loss: 3.4938 - accuracy: 0.0545 - 2s/epoch - 6ms/step

Since I had no idea where to begin, I started with the same as what Brian on his *Handwriting CNN* for my first model. The result was not pleasing. I tried running it twice just in case and both of the accuracy around 5%. Using CNN that could handle black and white was clearly did not work on color project like this. This needed to be improved.

---

### Model No. 2

Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(128 neurons) + Dropout(0.5)

- **Result 2_1**: 2s - loss: 0.1147 - accuracy: 0.9710 - 2s/epoch - 7ms/step
- **Result 2_2**: 2s - loss: 0.1222 - accuracy: 0.9673 - 2s/epoch - 7ms/step
- **Result 2_3**: 2s - loss: 0.1779 - accuracy: 0.9488 - 2s/epoch - 7ms/step

I recalled from the lecture that Brian mentioned adding an extra layer of convolution and pooling before flattening. I used that to create my second model by doubling another layer of the convolution and pooling with the same variables. The result improved drastically. I ran the code three times to see how steady it could be. The three accuracies swing from 95-97%. The difference between the min and max accuracies was at 0.0222.

---

### Model No. 3

Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(256 neurons) + Dropout(0.5)

- **Result 3**: 2s - loss: 0.2260 - accuracy: 0.9409 - 2s/epoch - 7ms/step

Then I tried doubling the hidden layers from 128 to 256 neurons as my third model. The result was not that much different. With 94% accuracy, I stopped the test for this model right there. Considering the amount of resources used, this might not worth it.

---

### Model No. 4

Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Convolution(64 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(128 neurons) + Dropout(0.5)

- **Result 4_1**: 3s - loss: 0.1033 - accuracy: 0.9724 - 3s/epoch - 8ms/step
- **Result 4_2**: 3s - loss: 0.1635 - accuracy: 0.9574 - 3s/epoch - 8ms/step
- **Result 4_3**: 3s - loss: 0.1409 - accuracy: 0.9625 - 3s/epoch - 8ms/step

Recalling from the lecture, Brian mentioned the first convolutaion and pooling layer might filter some larger aspects of the photos while the second layer will filter a finer aspects of the photos. I adjusted accordingly with the convolution in the second layer to be 64 filters, doubling the original value. The result was slightly better at 96-97% accuracy. It had become a bit steadier with difference between the min and max accuracies at 0.0150.

---

### Model No. 5

Convolution(64 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Convolution(64 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(128 neurons) + Dropout(0.5)

- **Result 5**: 4s - loss: 0.2014 - accuracy: 0.9521 - 4s/epoch - 11ms/step

Out of curiosity, what if I also doubled the amount of filters on the convolution in the first layer, so I did it. The result was not much different. The loss had increased quite a bit. So, no for this model.

---

### Model No. 6

Convolution(64 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(128 neurons) + Dropout(0.5)

- **Result 6**: 3s - loss: 0.4128 - accuracy: 0.8795 - 3s/epoch - 10ms/step

Another curiosity, what if I inverted the amount of filters for the first convolutional to be 64 and 32 for the second one. As expected, the result had become worse, less accuracy and more loss. Again, no for this model.

---

### Model No. 7

Convolution(32 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Convolution(64 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(128 neurons) + Dropout(0.4)

- **Result 7_1**: 3s - loss: 0.0847 - accuracy: 0.9780 - 3s/epoch - 8ms/step
- **Result 7_2**: 3s - loss: 0.0896 - accuracy: 0.9779 - 3s/epoch - 8ms/step
- **Result 7_3**: 3s - loss: 0.0755 - accuracy: 0.9811 - 3s/epoch - 8ms/step

I looked to tweak another variable and I picked the dropout rate. I tried reducing it to 0.4 this time but kept the other configurations from the best model so far, Model No. 4. This time the result was even better and steadier. The accuracy was 97-98% with the difference between min and max accuracies at 0.0032. The numbers for losses were also better.

---

### Model No. 8

Convolution(32 filters, 3x3 kernel) + Max Pooling(3x3) +<br>
Convolution(64 filters, 3x3 kernel) + Max Pooling(2x2) +<br>
Hidden Layers(128 neurons) + Dropout(0.4)

- **Result 8**: 2s - loss: 0.1625 - accuracy: 0.9573 - 2s/epoch - 6ms/step

Model No. 7 was very good but I wanted to try one more thing. If I changed the size of max pooling, what would happen? I changed the first max pooling size to be 3x3 and kept the rest from Model No.7 as my Model No.8. The result was less effective. It had less accuracy and more loss than Model No.7. Thus, Model No. 7 had the best result and I kept Model No.7 as my final solution.