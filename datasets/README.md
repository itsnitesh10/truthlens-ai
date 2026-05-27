# TruthLens AI — Datasets

## Text Datasets

### FakeNewsNet
- URL: https://github.com/KaiDMML/FakeNewsNet
- Contains: PolitiFact + GossipCop fake/real news
- Usage: Fine-tune text classifier

### LIAR Dataset
- URL: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip
- Contains: 12.8K labeled statements (pants-fire to true)
- Usage: Multi-class credibility classification

### ISOT Fake News Dataset
- URL: https://www.uvic.ca/ecs/ece/isot/assets/docs/ISOT_Fake_News_Dataset_ReadMe.pdf
- Contains: 23K+ articles (fake + real)
- Usage: Binary fake news classification

---

## Image Datasets

### CASIA Image Tampering Dataset
- URL: https://github.com/namtpham/casia2groundtruth
- Contains: Tampered images with ground truth masks
- Usage: ELA + forgery detection training

### FaceForensics++
- URL: https://github.com/ondyari/FaceForensics
- Contains: 1000+ deepfake videos + images
- Usage: Deepfake image face detection
- Note: Requires research agreement

---

## Video Datasets

### DeepFake Detection Challenge (DFDC)
- URL: https://ai.facebook.com/datasets/dfdc/
- Contains: 128K+ clips (real + deepfake)
- Usage: Video deepfake classification
- Note: Large download (~470GB)

### FaceForensics++ Video
- Same as above — includes video sequences

---

## Quick Start Data (Small)

For quick testing without downloading large datasets:
- Use any news article text from a website
- Use any JPEG image (photos with faces work best)
- Use any short MP4 video clip

---

## Loading Helper

See `datasets/loader.py` for dataset preparation utilities.
