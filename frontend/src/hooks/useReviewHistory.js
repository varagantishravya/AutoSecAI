import { useState, useEffect, useCallback } from "react";
import api from "../services/api";

/**
 * Custom hook to fetch review history from the backend.
 *
 * Returns:
 *   reviews  — array of past review objects
 *   loading  — boolean indicating if the fetch is in progress
 *   error    — error message string or null
 *   refresh  — function to manually re-fetch
 */
export default function useReviewHistory(limit = 50) {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchReviews = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get("/review-history", {
        params: { limit },
      });
      setReviews(response.data);
    } catch (err) {
      console.error("Failed to fetch review history:", err);
      setError("Could not load review history. Is the backend running?");
      setReviews([]);
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchReviews();

    function handleAuthChange() {
      fetchReviews();
    }

    window.addEventListener("user-auth-changed", handleAuthChange);
    return () => window.removeEventListener("user-auth-changed", handleAuthChange);
  }, [fetchReviews]);


  return { reviews, loading, error, refresh: fetchReviews };
}
