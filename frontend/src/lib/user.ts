import { doc, getDoc, setDoc, updateDoc, arrayUnion, arrayRemove } from "firebase/firestore";
import { db } from "./firebase";
import type { Recipe } from "./types";

interface UserProfile {
  allergies: string[];
  favoriteRecipes: string[];
  savedRecipes: Record<string, Recipe>;
}

const DEFAULT_PROFILE: UserProfile = {
  allergies: [],
  favoriteRecipes: [],
  savedRecipes: {},
};

function userRef(uid: string) {
  return doc(db, "users", uid);
}

export async function getUserProfile(uid: string): Promise<UserProfile> {
  const snap = await getDoc(userRef(uid));
  if (!snap.exists()) return DEFAULT_PROFILE;
  const data = snap.data();
  return {
    allergies: data.allergies ?? [],
    favoriteRecipes: data.favoriteRecipes ?? [],
    savedRecipes: data.savedRecipes ?? {},
  };
}

export async function saveAllergies(uid: string, allergies: string[]): Promise<void> {
  const ref = userRef(uid);
  const snap = await getDoc(ref);
  if (snap.exists()) {
    await updateDoc(ref, { allergies });
  } else {
    await setDoc(ref, { ...DEFAULT_PROFILE, allergies });
  }
}

export async function toggleFavoriteRecipe(
  uid: string,
  recipeId: string,
  recipe: Recipe
): Promise<boolean> {
  const ref = userRef(uid);
  const snap = await getDoc(ref);

  if (!snap.exists()) {
    await setDoc(ref, {
      ...DEFAULT_PROFILE,
      favoriteRecipes: [recipeId],
      savedRecipes: { [recipeId]: recipe },
    });
    return true;
  }

  const favorites: string[] = snap.data().favoriteRecipes ?? [];
  const isFavorited = favorites.includes(recipeId);

  if (isFavorited) {
    // Remove from favorites and delete saved recipe data
    const savedRecipes = snap.data().savedRecipes ?? {};
    delete savedRecipes[recipeId];
    await updateDoc(ref, {
      favoriteRecipes: arrayRemove(recipeId),
      savedRecipes,
    });
  } else {
    // Add to favorites and save recipe data
    await updateDoc(ref, {
      favoriteRecipes: arrayUnion(recipeId),
      [`savedRecipes.${recipeId}`]: recipe,
    });
  }

  return !isFavorited;
}

export async function getFavoriteRecipes(uid: string): Promise<Recipe[]> {
  const profile = await getUserProfile(uid);
  const recipes: Recipe[] = [];
  for (const id of profile.favoriteRecipes) {
    const recipe = profile.savedRecipes[id];
    if (recipe) recipes.push(recipe);
  }
  return recipes;
}
