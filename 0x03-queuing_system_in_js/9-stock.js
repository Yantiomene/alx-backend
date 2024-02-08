import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

function getItemById(id) {
  const item = listProducts.find((obj) => obj.itemId === id);

  if(item) {
    return Object.fromEntries(Object.entries(item));
  }
}

const app = express();
const client = createClient();
const PORT = 1245;

async function reserveStockById(itemId, stock) {
  promisify(client.SET).bind(client)(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  promisify(client.GET).bind(client)(`item.${itemId}`);
}

app.get('/list_products', (_, res) => res.json(listProducts));

app.get('/list_products/:itemId(\\d+)', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId, 10);
  const item = getItemById(Number.parseInt(itemId, 10));

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0, 10))
    .then((reservedStock) => {
      item.currentQuantity = item.initialAvailableQuantity - reservedStock;
      res.json(item);
    });
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId, 10);
  const item = getItemById(Number.parseInt(itemId, 10));

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0, 10))
    .then((reservedStock) => {
      if (reservedStock >= item.initialAvailableQuantity) {
        res.json({ status: 'Not enough stock available', itemId });
        return;
      }
      reserveStockById(itemId, reservedStock + 1)
          .then(() => {
            res.json({ status: 'Reservation confirmed', itemId });
          });
    });
});

async function resetProductsStock() {
  await Promise.all(listProducts.map(async (item) => {
    const setAsync = promisify(client.SET).bind(client);
    await setAsync(`item.${item.itemId}`, 0);
  }));
}

app.listen(PORT, () => {
  resetProductsStock()
    .then(() => {
      console.log(`API available on localhost port ${PORT}`);
    });
});

export default app;
