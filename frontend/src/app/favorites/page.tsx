"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { getFavoriteRecipes } from "@/lib/user";
import { RecipeCard } from "@/components/RecipeCard";
import { Button } from "@/components/ui/Button";
import { SkeletonCard } from "@/components/ui/Skeleton";
import type { Recipe } from "@/lib/types";

export default function FavoritesPage() {
  const router = useRouter();
  const { isLoggedIn, uid, loading: authLoading } = useAuth();
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authLoading) return;

    if (!isLoggedIn || !uid) {
      setLoading(false);
      return;
    }

    getFavoriteRecipes(uid)
      .then((favs) => setRecipes(favs))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [isLoggedIn, uid, authLoading]);

  // Not logged in
  if (!authLoading && !isLoggedIn) {
    return (
      <main className="flex flex-col items-center pt-16 text-center">
        <svg className="h-12 w-12 text-muted" viewBox="0 0 24 24" fill="none" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
        </svg>
        <h2 className="mt-4 text-xl font-semibold">Sign in to save favorites</h2>
        <p className="mt-2 text-sm text-muted">
          Create an account to save your favorite recipes and access them anytime.
        </p>
        <Button className="mt-6" onClick={() => router.push("/")}>
          Sign In
        </Button>
      </main>
    );
  }

  // Loading
  if (loading) {
    return (
      <main>
        <h1 className="text-2xl font-bold tracking-tight">Your Favorites</h1>
        <p className="mt-1 text-sm text-muted">Loading your saved recipes...</p>
        <div className="mt-8 space-y-6">
          <SkeletonCard />
          <SkeletonCard />
        </div>
      </main>
    );
  }

  // No favorites
  if (recipes.length === 0) {
    return (
      <main className="flex flex-col items-center pt-16 text-center">
        <svg className="h-12 w-12 text-muted" viewBox="0 0 24 24" fill="none" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
        </svg>
        <h2 className="mt-4 text-xl font-semibold">No favorites yet</h2>
        <p className="mt-2 text-sm text-muted">
          Generate recipes and tap the heart to save your favorites here.
        </p>
        <Button className="mt-6" onClick={() => router.push("/")}>
          Start Scanning
        </Button>
      </main>
    );
  }

  const handleFavoriteChange = (recipeId: string, isFavorited: boolean) => {
    if (!isFavorited) {
      setRecipes((prev) => prev.filter((r) => r.id !== recipeId));
    }
  };

  return (
    <main>
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight">Your Favorites</h1>
        <p className="mt-1 text-sm text-muted">
          {recipes.length} saved recipe{recipes.length !== 1 ? "s" : ""}
        </p>
      </div>

      <div className="space-y-6">
        {recipes.map((recipe) => (
          <RecipeCard
            key={recipe.id}
            recipe={recipe}
            initialFavorited
            onFavoriteChange={handleFavoriteChange}
          />
        ))}
      </div>
    </main>
  );
}
