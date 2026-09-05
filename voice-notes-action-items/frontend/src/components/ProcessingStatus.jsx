export default function ProcessingStatus({ step }) {
  if (!step) return null;

  return (
    <div className="processing-status">
      <div className="spinner" />
      <span>{step}</span>
    </div>
  );
}
