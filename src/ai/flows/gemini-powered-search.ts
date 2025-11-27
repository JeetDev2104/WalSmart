// src/ai/flows/gemini-powered-search.ts
'use server';

/**
 * @fileOverview An AI agent that uses natural language to search for products.
 *
 * - geminiPoweredSearch - A function that handles the product search process.
 * - GeminiPoweredSearchInput - The input type for the geminiPoweredSearch function.
 * - GeminiPoweredSearchOutput - The return type for the geminiPoweredSearch function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';
import { products } from '@/lib/data';

const GeminiPoweredSearchInputSchema = z.object({
  query: z.string().describe('The user query to search for products.'),
});
export type GeminiPoweredSearchInput = z.infer<typeof GeminiPoweredSearchInputSchema>;

const GeminiPoweredSearchOutputSchema = z.object({
  products: z
    .array(z.string())
    .describe('A list of product names that match the user query.'),
});
export type GeminiPoweredSearchOutput = z.infer<typeof GeminiPoweredSearchOutputSchema>;

export async function geminiPoweredSearch(input: GeminiPoweredSearchInput): Promise<GeminiPoweredSearchOutput> {
  return geminiPoweredSearchFlow(input);
}

const productNames = products.map(p => p.name).join(', ');

const prompt = ai.definePrompt({
  name: 'geminiPoweredSearchPrompt',
  input: {schema: GeminiPoweredSearchInputSchema},
  output: {schema: GeminiPoweredSearchOutputSchema},
  prompt: `You are a product search assistant for a grocery store. The user will provide a
query, and you should return a list of product names that match the user
query.

AVAILABLE PRODUCTS:
${productNames}

INSTRUCTIONS:
1. You MUST ONLY return product names from the "AVAILABLE PRODUCTS" list above. Do not invent new product names.
2. If the user asks for a recipe (e.g. "sushi", "fried rice", "biryani"), return the ingredients from the list that are relevant for that dish.
   - For "Sushi": Look for "Sushi Rice", "Nori Seaweed Sheets", "Rice Vinegar", "Wasabi Paste", "Soy Sauce".
   - For "Fried Rice": Look for "Jasmine Rice", "Soy Sauce", "Large Eggs", "Frozen Peas", "Fresh Carrots", "Vegetable Oil", "Yellow Onion".
   - For "Biryani": Look for "Basmati Rice Premium Grade", "Boneless Chicken Breast", "Garam Masala Spice Blend", "Plain Yogurt", "Yellow Onion".
3. If the user searches for a general term (e.g. "rice"), return all relevant varieties (e.g. "Basmati Rice Premium Grade", "Jasmine Rice", "Sushi Rice").
4. Return the exact product names as they appear in the list.

User Query: {{{query}}}`,
});

const geminiPoweredSearchFlow = ai.defineFlow(
  {
    name: 'geminiPoweredSearchFlow',
    inputSchema: GeminiPoweredSearchInputSchema,
    outputSchema: GeminiPoweredSearchOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
