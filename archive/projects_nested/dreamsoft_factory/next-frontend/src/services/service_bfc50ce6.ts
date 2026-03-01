import { useEffect, useState } from 'react';
import api from '@/lib/api';

type Product = {
  id: string;
  name: string;
};

const CartComponent: React.FC = () => {
  const [carts, setCarts] = useState<any[]>([]);
  const [productToBeDeleted, setProductToBeDeleted] = useState<Product | null>(null);

  useEffect(() => {
    // Fetch carts data when component mounts
    fetchCarts();
  }, []);

  const fetchCarts = async () => {
    try {
      const response = await api.get('/carts');
      setCarts(response.data.carts);
    } catch (error) {
      console.error('Failed to fetch carts:', error);
      // Notification.error('Error fetching carts');
    }
  };

  const addToCart = async (product: Product) => {
    try {
      const response = await api.post('/carts', { productId: product.id });
      setCarts(response.data.carts);

      if (response.status === 201 || response.status === 409) {
        setProductToBeDeleted(product);
        deleteProduct(product).then(() => {
          window.dispatchEvent(new Event('Cart:copied'));
        }).catch((error) => {
          console.error('Failed to delete product:', error);
          // Notification.error('Error deleting product');
        });
      }
    } catch (error) {
      console.error('Failed to add product to cart:', error);
      // Notification.error('Error adding product to cart');
    }
  };

  const deleteProduct = async (product: Product) => {
    try {
      await api.delete(`/carts/products/${product.id}`);
    } catch (error) {
      console.error('Failed to delete product from cart:', error);
      throw new Error('Failed to delete product from cart');
    }
  };

  return (
    <>
      {/* Render carts and UI elements */}
      <button onClick={() => addToCart({ id: 'someProductId', name: 'Sample Product' })}>Add to Cart</button>
      {carts.map((cart) => (
        <div key={cart.id}>{cart.name}</div>
      ))}
    </>
  );
};

export default CartComponent;