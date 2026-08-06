# Robotic Desk Organization Dataset

This dataset was specifically constructed for object detection and desk organization tasks in desktop environments. It is designed for training visual recognition models, such as the YOLO series, to support robots in detecting common stationery items, books, and paper, estimating their poses, and extracting keypoints for manipulation. The dataset includes both single-object and multi-object scenes, with substantial variations in category combinations, mild occlusion, and backgrounds to enhance robustness and generalisation.

---

## 1. Dataset Overview

The dataset is designed for desk organization tasks and provides high-quality annotated images for visual perception. It covers the following **9 object categories** commonly found on desktops:

* **Book**
* **Paper**
* **Pen**
* **Straight ruler**
* **Triangle ruler** 
* **Eraser**
* **Lead case**
* **Box**
* **Pen holder**

The robotic desk organization task primarily focuses on the first seven categories, while boxes and pen holders are included as additional desktop objects.

All images are annotated with bounding boxes and are suitable for training YOLO11 and other object detectors.

---

## 2. Data Collection Rules

To enhance model generalisation and adaptability to real-world environments, the dataset was collected according to the following rules:

* **Scene types**: Both **single-object** and **multi-object** scenes are included.

  * **Single-object scenes**: Each image contains only one target object. Variations in shooting angle, distance, lighting conditions, external distractors (e.g., non-target items), and backgrounds (e.g., plain or textured desktops) are considered. Total: **2,820** images.
  * **Multi-object scenes**: Each image contains multiple objects and covers common category combinations (see Table 1). The objects are primarily independently placed or mildly occluded, without severe occlusion. Total: **8,333** images.
* **Category combinations**: Based on object co-occurrence patterns in real desktop environments, typical combinations involving two to five categories were designed to ensure that the model can handle complex object arrangements.
* **Imaging conditions**: Images were captured at different camera heights and viewing angles to simulate realistic robot viewpoints.

---

## 3. Dataset Composition

The dataset comprises **11,366** images in total and is divided into 6 subsets according to scene complexity and category combinations, as shown below:

| Subset ID | Category Combination Description                                                                                                                                          | Number of Images |
| :-------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------: |
| dataset_1 | Single-class scenes (each class individually)                                                                                                                             |       2,816      |
| dataset_2 | Two-class combinations: paper + pen; book + pen                                                                                                                           |       1,218      |
| dataset_3 | Three-class combinations: paper + pen + ruler; paper + pen + other stationery; book + pen + ruler; book + pen + other stationery; paper + book + pen                      |       3,512      |
| dataset_4 | Four-class combinations: paper + pen + ruler + other stationery; book + pen + ruler + other stationery; paper + book + pen + ruler; paper + book + pen + other stationery |       2,842      |
| dataset_5 | Five-class combination: paper + book + pen + ruler + other stationery                                                                                                     |        761       |
| dataset_6 | Pure-background images (no target objects)                                                                                                                                |        217       |

> **Note**: “Other stationery” includes only erasers and lead cases. The “ruler” category includes both straight rulers and triangle rulers.

The subsets range from simple to complex scenes, providing substantial sample diversity for model training.

---

## 4. Annotation Tool and Format

* **Annotation tool**: [LabelImg](https://github.com/tzutalin/labelImg) was used for manual bounding-box annotation.
* **Original format**: Annotations are stored in **PASCAL VOC format** as XML files, with one annotation file corresponding to each image and sharing the same filename.
* **Conversion for training**: Since YOLO models require a specific annotation format, please convert the VOC XML files into **YOLO format**. Each image corresponds to one `.txt` file, with each line containing `class_id x_center y_center width height`, where all coordinates are normalised.

---

## 5. Annotation Rules

To ensure annotation consistency and effective model training, annotators follow these rules:

* **Overlapping objects**: When two target objects overlap, annotate the full bounding box of each object as long as less than half of the object is occluded. If more than half of the object is occluded, it should not be annotated.
* **Image quality**: Do not annotate images that are blurry, with indistinguishable object contours; too dark; overexposed; or otherwise unsuitable for object recognition. Images that do not meet the project-specific criteria, such as non-desktop scenes or scenes containing objects outside the 9 target classes, should also not be annotated.
* **Small objects**: Small objects, such as lead cases and erasers, should be annotated as long as their approximate boundaries can be distinguished by the human eye, regardless of their detectability by the algorithm.

---

## 6. Dataset Split and Performance Results

For the reported model training and evaluation, a selected subset of the dataset was used. This subset contained **2,816 single-class images** and **5,793 multi-class images**, with the multi-class images limited to scenes captured on green and red desktop backgrounds. The selected images were randomly divided into **80% training, 10% validation, and 10% test** sets.

A YOLO11 model trained on this subset achieved the following performance on the test set:

| Class     | Images | Instances | Box(P) |     R | mAP50 | mAP50-95 |
| --------- | -----: | --------: | -----: | ----: | ----: | -------: |
| all       |    862 |      2930 |  0.999 | 0.999 | 0.995 |    0.951 |
| eraser    |    210 |       239 |  1.000 | 1.000 | 0.995 |    0.893 |
| pen       |    598 |      1267 |  0.997 | 0.994 | 0.995 |    0.935 |
| paper     |    380 |       397 |  1.000 | 1.000 | 0.995 |    0.994 |
| book      |    427 |       441 |  0.999 | 1.000 | 0.995 |    0.995 |
| ruler     |    142 |       162 |  0.998 | 1.000 | 0.995 |    0.963 |
| lead case |    147 |       170 |  0.999 | 1.000 | 0.995 |    0.924 |
| triangle  |    218 |       254 |  0.999 | 1.000 | 0.995 |    0.955 |

> Speed per image: preprocessing, 0.2 ms; inference, 2.0 ms; post-processing, 0.6 ms.

The results show that the model achieves extremely high detection accuracy across all evaluated categories, with near-perfect performance for books, paper, rulers, and other objects.

---

## 7. Dataset Download

The dataset, together with the supporting code and pre-trained weights, is available on the project’s Releases page:

**Download URL**: [https://github.com/manipulation20/robotic-desk-organization/releases](https://github.com/manipulation20/robotic-desk-organization/releases)

After downloading and extracting the archive, please follow the instructions above for annotation-format conversion and dataset splitting. If you use this dataset in your research or project, please cite the associated paper. Citation details are available on the project homepage.

---

For questions or suggestions, please feel free to open an issue or contact us through the project repository. We hope you find this dataset useful!
