import ErrorAlert from "./ErrorAlert";
import LoadingIndicator from "./LoadingIndicator";

function StatusBar({ isLoading, error }) {
  return (
    <div className="flex items-center gap-1">
      {isLoading && <LoadingIndicator />}
      {error && <ErrorAlert error={error} />}
    </div>
  );
}

export default StatusBar;
