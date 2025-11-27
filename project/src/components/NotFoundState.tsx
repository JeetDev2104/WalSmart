import React from 'react';
import { motion } from 'framer-motion';
import { SearchX } from 'lucide-react';

interface NotFoundStateProps {
  type: 'product' | 'recipe' | 'general';
  query?: string;
}

const NotFoundState: React.FC<NotFoundStateProps> = ({ type, query }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex flex-col items-center justify-center py-16 text-center"
    >
      <motion.div
        initial={{ scale: 0.8, rotate: -10 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ 
          type: "spring",
          stiffness: 260,
          damping: 20,
          duration: 1.5
        }}
        className="mb-6 relative"
      >
        <div className="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center">
          <SearchX className="w-16 h-16 text-gray-400" />
        </div>
        <motion.div 
          animate={{ 
            y: [0, -10, 0],
            opacity: [0.5, 1, 0.5] 
          }}
          transition={{ 
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute -top-2 -right-2 text-4xl"
        >
          🤔
        </motion.div>
      </motion.div>

      <h3 className="text-2xl font-bold text-gray-900 mb-2">
        {type === 'recipe' 
          ? "We couldn't find all ingredients for this recipe"
          : `No results found for "${query}"`}
      </h3>
      
      <p className="text-gray-500 max-w-md mb-8">
        {type === 'recipe'
          ? "Some ingredients might be out of stock or not available in our catalog yet. Try searching for individual items."
          : "Try checking your spelling or using more general keywords. Our AI is still learning!"}
      </p>

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => window.location.reload()}
        className="px-6 py-2 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 transition-colors"
      >
        Refresh Catalog
      </motion.button>
    </motion.div>
  );
};

export default NotFoundState;
