export default function ErrorAlert({ error }) {
  return (
    <div
      className="w-full bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"
      role="alert"
    >
      <strong className="font-bold">Error: </strong>
      <span className="block sm:inline">
        {error.message || JSON.stringify(error)}
      </span>
    </div>
  );
}
