# Training Process Documentation

## Overview
This document provides a detailed account of the training process undertaken for fine-tuning the `microsoft/DialoGPT-medium` model, including preprocessing steps, training configuration, troubleshooting, and final outcomes.

---

## Steps Undertaken

### 1. **Dataset Preparation**
- **Dataset Source**: `fine_tune_dataset.json`
- **Dataset Structure**:
  ```json
  {
      "train": [
          {
              "instruction": "What is this about? What is Mindfulness?",
              "response": "Mindfulness is the basic human ability to be fully present..."
          },
          {
              "instruction": "How to practice Mindfulness?",
              "response": "Simple mindfulness exercises can be practiced anywhere..."
          }
      ]
  }
  ```
- **Conversion**: The dataset was loaded as a `Dataset` object using `Dataset.from_list()`.

### 2. **Preprocessing**
- **Preprocessing Function**:
  Tokenized inputs (`instruction`) and outputs (`response`) with the following configurations:
  - `truncation=True`
  - `padding="max_length"`
  - `max_length=512`

  Example function:
  ```python
  def preprocess_function(examples):
      inputs = tokenizer(
          examples["instruction"],
          truncation=True,
          padding="max_length",
          max_length=512
      )
      with tokenizer.as_target_tokenizer():
          outputs = tokenizer(
              examples["response"],
              truncation=True,
              padding="max_length",
              max_length=512
          )
      inputs["labels"] = outputs["input_ids"]
      inputs["labels"] = [
          -100 if token == tokenizer.pad_token_id else token
          for token in inputs["labels"]
      ]
      return inputs
  ```

- Applied preprocessing using `dataset.map(preprocess_function, batched=True)`.
- Converted dataset into PyTorch tensors: `tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])`.

### 3. **Data Splitting**
- **Split Method**: `train_test_split(test_size=0.2)`.
  - **Training Set**: 80%
  - **Evaluation Set**: 20%

---

## Training Configuration

### Model and Tokenizer
- **Pre-trained Model**: `microsoft/DialoGPT-medium`
- **Tokenizer Configuration**:
  - Padding token: `tokenizer.pad_token = tokenizer.eos_token`

### Training Arguments
```python
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=4e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_dir="./logs",
    push_to_hub=False,
    remove_unused_columns=False
)
```

### Data Collator
- Used `DataCollatorForSeq2Seq` for padding and alignment.

```python
data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
    padding="longest",
    max_length=512
)
```

### Metrics Function
- Computed evaluation metrics such as accuracy.

```python
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    return {"accuracy": (predictions == labels).mean()}
```

### Trainer
- **Trainer Initialization**:
  ```python
  trainer = Trainer(
      model=model,
      args=training_args,
      train_dataset=train_dataset,
      eval_dataset=eval_dataset,
      tokenizer=tokenizer,
      data_collator=data_collator,
      compute_metrics=compute_metrics
  )
  ```

- **Training Command**:
  ```python
  trainer.train()
  ```

### Model Saving
- Saved the fine-tuned model and tokenizer:
  ```python
  model.save_pretrained("trainers/fine_tuned_model")
  tokenizer.save_pretrained("trainers/fine_tuned_model")
  ```

---

## Issues and Resolutions

### 1. **Padding and Truncation Errors**
- **Error**:
  `Unable to create tensor, you should probably activate truncation and/or padding.`
- **Resolution**: Ensured `padding="max_length"` and `truncation=True` during tokenization.

### 2. **Slow Tensor Conversion**
- **Warning**:
  `Creating a tensor from a list of numpy.ndarrays is extremely slow.`
- **Resolution**: Converted lists directly to `numpy.ndarray` before creating tensors.

### 3. **Evaluation Metric Issues**
- **Observation**: Evaluation accuracy and loss fluctuated across runs.
- **Resolution**: Reviewed preprocessing steps, ensured consistent data splits, and set random seeds to ensure reproducibility.

---

## Metrics

### First Attempt:
- `eval_loss`: 2.3629
- `eval_accuracy`: 87.5%

### Latest Attempt:
- **Epoch 1**:
  - `eval_loss`: 2.8765
  - `eval_accuracy`: 80.4%
- **Epoch 2**:
  - `eval_loss`: 2.9913
  - `eval_accuracy`: 80.4%
- **Epoch 3**:
  - `eval_loss`: 2.8857
  - `eval_accuracy`: 80.4%

---

## Observations
- The first attempt achieved better evaluation metrics due to differences in preprocessing and handling of labels.
- Adjustments in data handling (e.g., label alignment) may have introduced noise affecting evaluation metrics.
- Consistency in dataset splitting and preprocessing is crucial for fair performance comparison.

---

## Recommendations
- Maintain a consistent pipeline across experiments.
- Revisit the preprocessing steps from the first run for optimal performance.
- Experiment with hyperparameter tuning (e.g., learning rate, batch size) to achieve better results.

---

## Next Steps
- Analyze evaluation dataset for potential inconsistencies.
- Fine-tune preprocessing and data collation methods.
- Explore additional epochs or alternative models for further improvements.

