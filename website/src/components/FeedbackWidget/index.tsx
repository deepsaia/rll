import React, {useState} from 'react';
import styles from './styles.module.css';

type Rating = 'helpful' | 'not-helpful' | null;

export default function FeedbackWidget(): React.JSX.Element {
  const [rating, setRating] = useState<Rating>(null);

  const handleFeedback = (value: Rating): void => {
    setRating(value);

    const page = typeof window !== 'undefined' ? window.location.pathname : '';
    console.log(`Feedback: ${value} on ${page}`);
  };

  if (rating !== null) {
    const message =
      rating === 'helpful'
        ? 'Thanks for your feedback!'
        : 'Thanks for your feedback! Help us improve.';

    return (
      <div className={styles.feedbackWidget}>
        <p className={styles.thankYou}>
          {message}
          {rating === 'not-helpful' && (
            <>
              {' '}
              <a
                href={`https://github.com/deepsaia/rll/issues/new?title=${encodeURIComponent('[Feedback] ' + (typeof document !== 'undefined' ? document.title : ''))}&body=${encodeURIComponent('Page: ' + (typeof window !== 'undefined' ? window.location.href : '') + '\n\nWhat was missing or confusing?')}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                Open an issue
              </a>
            </>
          )}
        </p>
      </div>
    );
  }

  return (
    <div className={styles.feedbackWidget}>
      <p className={styles.prompt}>Was this page helpful?</p>
      <div className={styles.buttons}>
        <button
          className={styles.feedbackButton}
          onClick={() => handleFeedback('helpful')}
          title="This page was helpful"
          type="button"
        >
          👍
        </button>
        <button
          className={styles.feedbackButton}
          onClick={() => handleFeedback('not-helpful')}
          title="This page could be improved"
          type="button"
        >
          👎
        </button>
      </div>
    </div>
  );
}
