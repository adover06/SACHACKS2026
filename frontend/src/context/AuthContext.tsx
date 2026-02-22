"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import {
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut as firebaseSignOut,
  updateProfile,
  type User,
} from "firebase/auth";
import { auth } from "@/lib/firebase";

interface GuestSession {
  type: "guest";
  id: string;
}

interface AuthState {
  user: User | null;
  guest: GuestSession | null;
  loading: boolean;
  isAuthenticated: boolean;
  isLoggedIn: boolean;
  displayName: string | null;
  uid: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
  continueAsGuest: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

const GUEST_KEY = "sss_guest_session";
const googleProvider = new GoogleAuthProvider();

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [guest, setGuest] = useState<GuestSession | null>(null);
  const [loading, setLoading] = useState(true);

  // Listen to Firebase auth state
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      if (firebaseUser) {
        localStorage.removeItem(GUEST_KEY);
        setGuest(null);
      }
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  // Restore guest session from localStorage
  useEffect(() => {
    if (!user) {
      const stored = localStorage.getItem(GUEST_KEY);
      if (stored) {
        try {
          setGuest(JSON.parse(stored));
        } catch {
          localStorage.removeItem(GUEST_KEY);
        }
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const signIn = useCallback(async (email: string, password: string) => {
    await signInWithEmailAndPassword(auth, email, password);
  }, []);

  const signUp = useCallback(
    async (email: string, password: string, name: string) => {
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(cred.user, { displayName: name });
    },
    []
  );

  const signInWithGoogle = useCallback(async () => {
    await signInWithPopup(auth, googleProvider);
  }, []);

  const signOut = useCallback(async () => {
    await firebaseSignOut(auth);
    localStorage.removeItem(GUEST_KEY);
    setGuest(null);
  }, []);

  const continueAsGuest = useCallback(() => {
    const session: GuestSession = {
      type: "guest",
      id: `guest_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
    };
    localStorage.setItem(GUEST_KEY, JSON.stringify(session));
    setGuest(session);
  }, []);

  const isAuthenticated = !!user || !!guest;
  const isLoggedIn = !!user;
  const displayName = user?.displayName ?? (guest ? "Guest" : null);
  const uid = user?.uid ?? guest?.id ?? null;

  return (
    <AuthContext.Provider
      value={{
        user,
        guest,
        loading,
        isAuthenticated,
        isLoggedIn,
        displayName,
        uid,
        signIn,
        signUp,
        signInWithGoogle,
        signOut,
        continueAsGuest,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
