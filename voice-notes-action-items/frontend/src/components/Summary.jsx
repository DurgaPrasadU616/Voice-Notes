export default function Summary({ text }) {
  if (!text) return null;

  return (
    <div className="summary-block">
      <h3>Summary</h3>
      <p>{text}</p>
    </div>
  );
}
