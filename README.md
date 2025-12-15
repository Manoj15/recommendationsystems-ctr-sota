# RecommendationSystems_Criteo_SOTA
Experimenting SOTA Recommnedation Algorithms on Criteo Benchmarking Dataset



📊 Dataset Overview

This project uses the Microsoft News Dataset (MIND), a large-scale public benchmark released by Microsoft for research in news recommendation and personalized ranking systems. The dataset contains rich user behavior logs, detailed item (news) metadata, and explicit impression-level interactions, making it one of the most realistic publicly available datasets for studying modern recommender systems.

Unlike many traditional recommendation datasets that only capture post-hoc interactions (such as ratings or purchases), MIND provides impression-level data, including both clicked and non-clicked items. This allows models to learn from true user choice behavior, which is critical for ranking and click-through-rate (CTR) prediction tasks.

🎯 Why This Dataset Is Relevant for Recommendation Systems

The MIND dataset is particularly valuable because it supports end-to-end recommendation research, from representation learning to ranking evaluation:

Rich Item Metadata
Each news article includes a title, abstract, category, sub-category, and entity annotations. This enables text-aware and content-based recommendation, including modern approaches using Transformer or LLM-based embeddings.

User Interaction Histories
The dataset provides sequential user reading histories, allowing models to capture short-term and long-term user interests, which is essential for personalized recommendations.

Impression-Level Interaction Logs
For each user session, the dataset records which items were shown and which were clicked. This makes it suitable for ranking and CTR prediction, not just implicit feedback modeling.

Realistic Recommendation Setting
The combination of user context, item content, and exposure-aware interactions closely mirrors real-world recommendation and advertising systems used in production environments.

Because of these properties, MIND is widely used as a benchmark for:

Personalized ranking models

Sequential and session-based recommenders

Text-aware and LLM-based recommendation systems

Click-through-rate prediction with rich content features

🔍 Typical Use Cases

Learning user and item embeddings from textual content

Evaluating ranking models using click vs. non-click impressions

Studying user interest evolution over time

Benchmarking content-aware and hybrid recommendation architectures