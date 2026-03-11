import api from '@/lib/api';
import { useEffect, useState } from 'react';

interface ScrollToTopProps {
  offset: number;
  duration: number;
}

const ScrollToTop = ({ offset, duration }: ScrollToTopProps) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
      // For iOS devices
      const handleTouchEvents = () => {
        if ($(window).scrollTop() > offset) {
          $('.scroll-to-top').fadeIn(duration);
          setIsVisible(true);
        } else {
          $('.scroll-to-top').fadeOut(duration);
          setIsVisible(false);
        }
      };

      $(window).on('touchend touchcancel touchleave', handleTouchEvents);

      // Cleanup function
      return () => {
        $(window).off('touchend touchcancel touchleave', handleTouchEvents);
      };
    } else {
      const handleScroll = () => {
        if ($(window).scrollTop() > offset) {
          $('.scroll-to-top').fadeIn(duration);
          setIsVisible(true);
        } else {
          $('.scroll-to-top').fadeOut(duration);
          setIsVisible(false);
        }
      };

      $(window).on('scroll', handleScroll);

      // Cleanup function
      return () => {
        $(window).off('scroll', handleScroll);
      };
    }

  }, [offset, duration]);

  return (
    <div className="scroll-to-top" style={{ display: isVisible ? 'block' : 'none' }}>
      {/* Your scroll to top button content */}
    </div>
  );
};

export default ScrollToTop;

// Example of the Credit Limit Info function in a Next.js context
interface LoggedUser {
  logged: boolean;
}

const useGetCreditLimitInfo = (loggedUser: LoggedUser) => {
  const [creditLimit, setCreditLimit] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error>();

  useEffect(() => {
    if (!loggedUser.logged) return;

    async function fetchCreditLimit() {
      try {
        const response = await api.get('/credit-limit'); // Adjust the endpoint as necessary
        setCreditLimit(response.data.credit_limit); // Assuming credit limit is in the data object
      } catch (err: any) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    fetchCreditLimit();
  }, [loggedUser.logged]);

  return { loading, error, creditLimit };
};