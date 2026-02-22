import { Skeleton, SkeletonCard } from "@/components/ui/Skeleton";

export default function FavoritesLoading() {
  return (
    <main>
      <Skeleton className="h-8 w-44" />
      <Skeleton className="mt-2 h-4 w-48" />
      <div className="mt-8 space-y-6">
        <SkeletonCard />
        <SkeletonCard />
      </div>
    </main>
  );
}
