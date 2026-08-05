# Robotic Desk Organization Dataset

This dataset is specifically constructed for object detection and desk organization tasks in desktop scenarios. It is designed to train visual recognition models (e.g., YOLO series) to support robots in detecting common stationery, books, and paper items, estimating their poses, and extracting keypoints for manipulation. The dataset covers both single‑object and multi‑object scenes, with rich variations in category combinations, occlusion levels, and backgrounds, ensuring strong robustness and generalization.

---

## 1. Dataset Overview

The dataset targets the desk organization task and provides high‑quality annotated images for visual perception. It covers the **7 most common object categories** found on desktops:

- **Book**
- **Paper**
- **Pen**
- **Ruler**
- **Triangle** (set square)
- **Eraser**
- **Lead case** (pencil case / lead container)

All images are annotated with bounding boxes, suitable for training YOLO11 and other object detectors. A YOLO11 model trained on this dataset achieved **mAP@50 = 0.995** and **mAP@50:95 = 0.951** on the test set, demonstrating the high quality and representativeness of the annotations.

---

## 2. Data Collection Rules

To enhance model generalisation and real‑world adaptability, the dataset was collected following these rules:

- **Scene types**: Both **single‑object** and **multi‑object** scenes are included.
  - **Single‑object scenes**: Each image contains only one target object. Different shooting angles, distances, lighting conditions, external distractors (e.g., non‑target items), and backgrounds (plain desktop, textured desktop, etc.) are considered. Total: **2,820** images.
  - **Multi‑object scenes**: Each image contains multiple objects, covering common category combinations (see Table 1), with varying degrees of overlap (independent, slight overlap, heavy overlap). Total: **7,397** images.
- **Category combinations**: Based on co‑occurrence patterns in real desktop scenarios, 2‑ to 5‑category typical combinations were designed to ensure the model can handle complex arrangements.
- **Imaging conditions**: Images were captured under various lighting (natural light, indoor lighting), heights, and viewing angles to simulate real robot viewpoints.

---

## 3. Dataset Composition

The dataset comprises **10,217** images in total, divided into 6 subsets according to scene complexity and category combinations, as shown below:

| Subset ID | Category Combination Description | Number of Images |
| :-------: | :-------------------------------- | :--------------: |
| 1         | Single‑class scenes (each class individually) | 2,816 |
| 2         | Two‑class combinations: paper+pen; book+pen | 1,219 |
| 3         | Three‑class combinations: paper+pen+ruler; paper+pen+other stationery; book+pen+ruler; book+pen+other stationery; paper+book+pen | 3,513 |
| 4         | Four‑class combinations: paper+pen+ruler+other; book+pen+ruler+other; paper+book+pen+ruler; paper+book+pen+other | 2,842 |
| 5         | Five‑class combination: paper+book+pen+ruler+other | 761 |
| 6         | Pure background (no target objects) | 217 |

> **Note**: “Other stationery” includes erasers, lead cases, triangles, etc., i.e., categories other than paper, pen, book, and ruler.

The subsets span from simple to complex scenes, offering abundant sample diversity for model training.

---

## 4. Annotation Tool and Format

- **Annotation tool**: [LabelImg](https://github.com/tzutalin/labelImg) for manual bounding‑box annotation.
- **Original format**: Annotations are saved in **PASCAL VOC format** (XML files), one per image with the same name.
- **Conversion for training**: Since YOLO models require a specific format, please use the provided conversion script to transform VOC XML files into **YOLO format** (one `.txt` file per image, each line containing `class_id x_center y_center width height`, all normalised). The conversion script is available in the project code repository.

---

## 5. Annotation Rules

To ensure annotation consistency and training effectiveness, annotators must follow these rules:

- **Overlapping objects**: When two target objects overlap, annotate the full bounding box for each as long as the occluded area is **less than half of the object’s visible region**. If occlusion exceeds half, the object is not annotated.
- **Image quality**: Do not annotate images that are blurry (object contours indiscernible), too dark, or over‑exposed (objects unrecognisable), or those that do not meet project‑specific criteria (e.g., non‑desktop scenes or objects outside the 7 classes).
- **Small objects**: For small objects (e.g., lead cases, erasers), annotate them as long as human eyes can distinguish their approximate boundaries, regardless of algorithmic detectability.

---

## 6. Dataset Split and Performance Results

The dataset was randomly split into **80% training, 10% validation, and 10% test** sets. A YOLO11 model trained on this dataset achieved the following performance on the test set:

| Class      | Images | Instances | Box(P) | R    | mAP50 | mAP50-95 |
|------------|--------|-----------|--------|------|-------|----------|
| all        | 862    | 2930      | 0.999  | 0.999| 0.995 | 0.951    |
| eraser     | 210    | 239       | 1.000  | 1.000| 0.995 | 0.893    |
| pen        | 598    | 1267      | 0.997  | 0.994| 0.995 | 0.935    |
| paper      | 380    | 397       | 1.000  | 1.000| 0.995 | 0.994    |
| book       | 427    | 441       | 0.999  | 1.000| 0.995 | 0.995    |
| ruler      | 142    | 162       | 0.998  | 1.000| 0.995 | 0.963    |
| lead case  | 147    | 170       | 0.999  | 1.000| 0.995 | 0.924    |
| triangle   | 218    | 254       | 0.999  | 1.000| 0.995 | 0.955    |

> Speed per image: preprocessing 0.2ms, inference 2.0ms, post‑processing 0.6ms.

The results show that the model achieves extremely high detection accuracy for all categories, with near‑perfect performance on books, paper, rulers, etc.

---

## 7. Dataset Download

The dataset, along with supporting code and pre‑trained weights, is available on the project’s Releases page:

**Download URL**: [https://github.com/manipulation20/robotic-desk-organization/releases](https://github.com/manipulation20/robotic-desk-organization/releases)

After downloading and extracting the archive, please follow the instructions above for format conversion and dataset splitting. If you use this dataset in your research or project, please cite the associated paper (see the project homepage for details).

---

For any questions or suggestions, feel free to open an issue or contact us via the project repository. Enjoy using the dataset!