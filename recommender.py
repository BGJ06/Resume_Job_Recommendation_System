import pandas as pd
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import clean_text


class JobRecommender:

    def __init__(self):
        self.jobs_df = None
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
        self.job_vectors = None

    def load_data(self):
        # Load datasets
        jobs1 = pd.read_csv(
            "datasets/file2.csv",
            usecols=[
                "title",
                "company",
                "experience",
                "salary",
                "location",
                "job-description",
                "skills",
            ],
        ).sample(n=5000, random_state=42)

        jobs2 = pd.read_csv(
            "datasets/file3.csv",
            usecols=[
                "title",
                "description",
                "skills",
            ],
        ).sample(n=5000, random_state=42)

        # Standardize columns for file3
        jobs2 = jobs2.rename(columns={
            "description": "job-description"
        })

        # Add missing columns if not present
        for col in ["company", "experience", "salary", "location", "skills"]:
            if col not in jobs2.columns:
                jobs2[col] = "Not Available"

        # Keep common columns
        cols = ["title", "company", "experience",
                "salary", "location",
                "job-description", "skills"]

        jobs1 = jobs1[cols]
        jobs2 = jobs2[cols]

        # Merge datasets
        self.jobs_df = pd.concat([jobs1, jobs2], ignore_index=True)

        # Fill missing values
        self.jobs_df = self.jobs_df.fillna("")

        # Create combined text
        self.jobs_df["combined"] = (
            self.jobs_df["title"].astype(str) + " " +
            self.jobs_df["skills"].astype(str) + " " +
            self.jobs_df["job-description"].astype(str)
        )

        # Clean text
        self.jobs_df["combined"] = self.jobs_df["combined"].apply(clean_text)

        # TF-IDF
        self.job_vectors = self.vectorizer.fit_transform(
            self.jobs_df["combined"]
        )

    def recommend_jobs(self, resume_text, top_n=5):

        resume_text = clean_text(resume_text)

        resume_vector = self.vectorizer.transform([resume_text])

        similarity = cosine_similarity(
            resume_vector,
            self.job_vectors
        ).flatten()

        top_indices = similarity.argsort()[-top_n:][::-1]

        recommendations = []

        for idx in top_indices:

            row = self.jobs_df.iloc[idx]

            recommendations.append({
                "title": row["title"],
                "company": row["company"],
                "experience": row["experience"],
                "salary": row["salary"],
                "location": row["location"],
                "skills": row["skills"],
                "score": round(similarity[idx] * 100, 2)
            })

        return recommendations