export default function LoadingIndicator() {
  return (
    <div className="flex items-center">
      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
      <span className="ml-2">Loading...</span>
    </div>
  );
}
