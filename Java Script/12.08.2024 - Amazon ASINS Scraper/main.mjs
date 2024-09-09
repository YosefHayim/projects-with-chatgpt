import puppeteer from 'puppeteer';
import Client from '@infosimples/node_two_captcha';
import readline from 'readline';
import fs from 'fs'
import path from 'path';

let logFilePath;
function logMessage(message) {
  // Function to get a timestamp string for the log file name (YYYY-MM-DD_HH-MM-SS)
  function getLogFileName() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); 
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `log_${day}-${month}-${year}_${hours}-${minutes}-${seconds}.txt`;
  }

  // If logFilePath is not set, initialize it with the current date and time's log file
  if (!logFilePath) {
    const logFileName = getLogFileName(); // Filename based on the current date and time
    logFilePath = path.join('C:\\Github\\Javascript-Projects\\12.08.2024 - Amazon ASINS Scraper\\logs', logFileName);
  }

  // Log to console
  console.log(message);

  // Log to file
  fs.appendFileSync(logFilePath, `${new Date().toISOString()} - ${message}\n`);
}

async function promptUser(query) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => rl.question(query, (answer) => {
    rl.close();
    resolve(answer);
  }));
}

async function getAmazon() {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  // Go to the Amazon page
  await page.goto('https://amazon.com/');
  return page;
}

async function isCaptcha(page) {
  try {
    // Wait for the specific captcha text selector
    const captcha_text = await page.waitForSelector('body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-row.a-spacing-large > div > div > h4', { timeout: 5000 });
    
    // If the captcha selector is found
    if (captcha_text) {
      logMessage(`Captcha popped up...`);
      
      // Wait for the actual img element and correctly target it
      await page.waitForSelector('body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-row.a-spacing-large > div > div > div.a-row.a-text-center img');

      // Now get the src attribute of the img element
      const imageUrl = await page.$eval('body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-row.a-spacing-large > div > div > div.a-row.a-text-center img', img => img.src);
      
      logMessage(`Captcha image URL: ${imageUrl}`);
      
      return imageUrl; // Return the image URL if found
    } else {
      logMessage(`No Captcha found.`);
      return null; // if no captcha img url found
    }
  } catch (error) {
    logMessage(`Error detecting Captcha: ${error}`); // if there was any error detected
    return null;
  }
}

async function solveCaptcha(page, imageUrl) {
  if (imageUrl) {
    const client = new Client('b4c7bb3916d01aa1fda30b90f6650e66', {
      timeout: 60000,
      polling: 5000,
      throwErrors: false
    });

    try {
      // log the balance of the account from 2captcha API
      client.balance().then(function(response) {
        logMessage(response);
      });
      const response = await client.decode({ url: imageUrl });
      const captchaResult = response.text;
      logMessage(`Captcha Result: ${captchaResult}`);
      
      // Now insert the captchaResult into the captcha input
      await page.type('#captchacharacters', captchaResult);

      // Optionally wait for the navigation if clicking causes a page load
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle0' }), // Wait for navigation to complete
        page.click('body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-section.a-spacing-extra-large > div > span > span > button')
      ]);
      logMessage(`Solved Captcha`);
      return captchaResult;
    } catch (error) {
      logMessage(`Error solving Captcha: ${error}`);
      return null;
    }
  }
  return null; // Return null if there's no imageUrl
}

async function zipcodeChange(page) {
  // Click on the zipcode button
  await page.click('#nav-global-location-popover-link');

  await new Promise(resolve => setTimeout(resolve, 1000));

  // Wait for the input field to be available and set its value
  await page.waitForSelector('#GLUXZipUpdateInput', { visible: true });

  await new Promise(resolve => setTimeout(resolve, 1000));

  await page.type('#GLUXZipUpdateInput', '33180');

  // Press Enter twice
  await page.keyboard.press('Enter');

  await new Promise(resolve => setTimeout(resolve, 1000));

  await page.keyboard.press('Enter');
}

async function searchTermByUser(page) {
  // Getting user input search term
  const searchTerm = await promptUser('Please enter the search term: ');

  // Finding the input search bar and type based on user result
  await page.type('#twotabsearchtextbox', searchTerm);
  await page.keyboard.press('Enter'); // Press Enter to search

  // Wait for the search results to load
  await page.waitForSelector('[data-asin]', { visible: true });

  // Calling userFilters function before we start the extraction
  await userFilters(page);

  return searchTerm; // Ensure the search term is returned
}

async function extractASINS(page) {
  // Persistent Set to store all unique ASINs across pages, initialized on the first call
  extractASINS.allAsins = extractASINS.allAsins || new Set();

  // Wait for all elements with the data-asin attribute to be present
  await page.waitForSelector('[data-asin]', { visible: true });

  // Optionally wait for additional time (e.g., for page load)
  await new Promise(resolve => setTimeout(resolve, 5000));

  // Execute the code in the page context to extract ASINs
  const asinSet = await page.evaluate(() => {
    const dataAsins = document.querySelectorAll('[data-asin]');
    const asinSet = new Set(); // Use a Set to store unique ASINs

    dataAsins.forEach(element => {
      const asin = element.getAttribute('data-asin');
      if (asin) {
        asinSet.add(asin);
      }
    });  
    return Array.from(asinSet); 
  });

  // Add the ASINs from this page to the cumulative set
  asinSet.forEach(asin => extractASINS.allAsins.add(asin));

  // Log the number of ASINs found on this page
  logMessage(`Asins Found on this page: ${asinSet.length}`);

  // Log the ASINs from this page
  logMessage(`ASINs on this page: ${asinSet.join(', ')}`);

  return Array.from(extractASINS.allAsins); // Return the cumulative ASINs
}

let currentPage = 1

async function goNextPage(page) {
  const totalPages = await page.$$eval('span.s-pagination-item.s-pagination-disabled[aria-disabled="true"]', elements => {
    return Math.max(...elements.map(el => parseInt(el.textContent.trim(), 10)));
  });

  // Log the current progress before navigating to the next page
  logMessage(`Total Pages: ${currentPage} / ${totalPages}`);

  const hasNextPage = await page.evaluate(() => {
    const nextButton = document.querySelector('.s-pagination-item.s-pagination-next');

    if (nextButton && !nextButton.classList.contains('s-pagination-disabled')) {
      nextButton.click();
      return true; 
    } else {
      return false;
    }
  });

  if (hasNextPage) {
    currentPage++;  // Increment the page number after clicking the next button
    logMessage(`Moving to next page: ${currentPage}`);
  } else {
    logMessage('Reached the last page or no next button available.');
  }

  return hasNextPage;
}

async function saveAsinsToCSV(searchTerm) {
  // Check if there are any ASINs to save
  if (!extractASINS.allAsins || extractASINS.allAsins.size === 0) {
    logMessage('No ASINs available to save.');
    return;
  }

  // Convert the Set to an array
  const asinArray = Array.from(extractASINS.allAsins);

  // Prepare the CSV content
  const csvContent = asinArray.join('\n');

  // Create the filename based on search term and number of ASINs found
  const sanitizedSearchTerm = searchTerm.replace(/[^a-z0-9]/gi, '_').toLowerCase();
  const fileName = `${sanitizedSearchTerm}_${asinArray.length}_asins.csv`;

  // Define the file path
  const filePath = path.join('C:\\Github\\Javascript-Projects\\12.08.2024 - Amazon ASINS Scraper\\History Asins', fileName);

  // Write the CSV content to a file
  fs.writeFileSync(filePath, csvContent);

  logMessage(`ASINs have been saved to ${filePath}`);
}

async function userFilters(page) {
  const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
  });

  // Helper function to ask questions and get a valid response (y or n)
  function askYesNoQuestion(query) {
      return new Promise((resolve) => {
          rl.question(query, (answer) => {
              answer = answer.trim().toLowerCase();
              if (answer === 'y' || answer === 'n') {
                  resolve(answer);
              } else {
                  logMessage("Please reply with 'y' or 'n'.");
                  resolve(askYesNoQuestion(query)); // Repeat the question if the answer is invalid
              }
          });
      });
  }

  // Helper function to ask for a number and validate it
  function askForNumber(query, validate) {
      return new Promise((resolve) => {
          rl.question(query, (answer) => {
              const number = parseFloat(answer);
              if (!isNaN(number) && validate(number)) {
                  resolve(number);
              } else {
                  logMessage("Please enter a valid number.");
                  resolve(askForNumber(query, validate)); // Repeat the question if the input is invalid
              }
          });
      });
  }
  const filters = {};

  // Question 1: Would you like products with 4+ stars?
  filters.fourPlusStars = await askYesNoQuestion("Would you like ASIN products with 4+ stars? (y/n): ");
  if (filters.fourPlusStars === 'y') {
    const firstLink = await page.$('a.a-link-normal.s-navigation-item section[aria-label="4 Stars & Up"]');
    if (firstLink) {
          await firstLink.click();
          logMessage("Clicked on '4 Stars & Up' filter.");
      } else {
          logMessage("'4 Stars & Up' filter not found.");
      }
  }
  
// Question 2: Would you like a specific price range?
const priceRange = await askYesNoQuestion("Would you like a specific price range? (y/n): ");
if (priceRange === 'y') {
    filters.priceRange = {};

    // First, check if there is a price slider
    const hasPriceSlider = await page.$('input#p_36\\2Frange-slider_slider-item_lower-bound-slider') !== null;

    if (hasPriceSlider) {
        // Retrieve the maximum price allowed from the page
        const maxAllowedPriceText = await page.$eval('input#p_36\\2Frange-slider_slider-item_upper-bound-slider', el => el.getAttribute('aria-valuetext'));
        const maxAllowedPrice = parseInt(maxAllowedPriceText.replace(/[^0-9]/g, ''), 10);

        filters.priceRange.startPrice = await askForNumber(
            "Enter the minimum price (0 or above): ",
            (number) => number >= 0
        );

        filters.priceRange.maxPrice = await askForNumber(
            `Enter the maximum price (at least ${filters.priceRange.startPrice + 10} and no more than ${maxAllowedPrice}): `,
            (number) => number >= filters.priceRange.startPrice && number <= maxAllowedPrice
        );

        // Set the price range in the Puppeteer context
        await page.evaluate((startPrice, maxPrice) => {
            // Set the minimum price
            document.querySelector('input#p_36\\2Frange-slider_slider-item_lower-bound-slider').value = startPrice;
            document.querySelector('input[name="low-price"]').value = startPrice;

            // Set the maximum price
            document.querySelector('input#p_36\\2Frange-slider_slider-item_upper-bound-slider').value = maxPrice;
            document.querySelector('input[name="high-price"]').value = maxPrice;

            // Click the submit button
            document.querySelector('input.a-button-input[type="submit"]').click();
        }, filters.priceRange.startPrice, filters.priceRange.maxPrice);

        logMessage(`Price range set to: ${filters.priceRange.startPrice} - ${filters.priceRange.maxPrice}`);

    } else {
        // Check if there are predefined price range options
        const priceOptions = await page.$$eval('#filter-p_n_price_fma li a span.a-size-base', elements => {
            return elements.map(el => el.textContent.trim());
        });

        if (priceOptions.length > 0) {
            // Present the options to the user
            logMessage("Predefined price ranges available:");
            priceOptions.forEach((option, index) => {
                logMessage(`${index + 1}: ${option}`);
            });

            const selectedOption = await askForNumber(
                `Select a price range (1-${priceOptions.length}): `,
                (number) => number >= 1 && number <= priceOptions.length
            );

            // Click the selected price range
            await page.evaluate((selectedIndex) => {
                document.querySelectorAll('#filter-p_n_price_fma li a')[selectedIndex - 1].click();
            }, selectedOption);

            logMessage(`Selected price range: ${priceOptions[selectedOption - 1]}`);
        } else {
            logMessage("No price filtering options are available for this category.");
        }
    }
} else {
    filters.priceRange = null; // No specific price range
}

  // Question 3: Want all discounts?
  filters.allDiscounts = await askYesNoQuestion("Want ASINS with most of discounts? (y/n): ");
  if (filters.allDiscounts === 'y') {
      const secondLink = await page.$('a.a-link-normal.s-navigation-item[href*="p_n_deal_type%3A23566065011"]');
      if (secondLink) {
          await secondLink.click();
          logMessage("Clicked on 'All Discounts' filter.");
      } else {
          logMessage("'All Discounts' filter not found.");
      }
  } else {
      // Question 4: Want today's deals?
      filters.todayDeals = await askYesNoQuestion("Want ASINS DEALS? (y/n): ");
      if (filters.todayDeals === 'y') {
          const thirdLink = await page.$('a.a-link-normal.s-navigation-item[href*="p_n_deal_type%3A23566064011"]');
          if (thirdLink) {
              await thirdLink.click();
              logMessage("Clicked on 'Today's Deals' filter.");
          } else {
              logMessage("'Today's Deals' filter not found.");
          }
      }
  }

  // Question 5: Want COUPON ASINS?
  filters.couponASINS = await askYesNoQuestion("Want COUPON ASINS? (y/n): ");
  while (filters.couponASINS !== 'y' && filters.couponASINS !== 'n') {
      logMessage("Please reply with 'y' or 'n'.");
      filters.couponASINS = await askYesNoQuestion("Want COUPON ASINS? (y/n): ");
  }

  if (filters.couponASINS === 'y') {
      logMessage("Scraping only coupon ASINs...");
      await findAsinsWithCoupons(page);
  } else {
      logMessage("Continue normal scraping...");
  }

  rl.close();
  logMessage(`Finished Filters Stage continue to scarping...`)
  return filters;
}

async function findAsinsWithCoupons(page) {
  // Persistent Set to store all unique ASINs with coupons across pages, initialized on the first call
  findAsinsWithCoupons.allAsins = findAsinsWithCoupons.allAsins || new Set();

  // Wait for all elements with the data-asin attribute to be present
  await page.waitForSelector('[data-asin]', { visible: true });

  // Optionally wait for additional time (e.g., for page load)
  await new Promise(resolve => setTimeout(resolve, 5000));

  // Execute the code in the page context to extract ASINs with coupons
  const asinSet = await page.evaluate(() => {
      const asinElements = document.querySelectorAll('[data-asin]');
      const asinSet = new Set(); // Use a Set to store unique ASINs

      asinElements.forEach(asinElement => {
          const asin = asinElement.getAttribute('data-asin');
          const couponElement = asinElement.querySelector('.s-coupon-unclipped');

          if (couponElement && /Save/.test(couponElement.textContent)) {
              asinSet.add(asin);
          }
      });

      return Array.from(asinSet);
  });

  // Add the ASINs with coupons from this page to the cumulative set
  asinSet.forEach(asin => findAsinsWithCoupons.allAsins.add(asin));

  return Array.from(findAsinsWithCoupons.allAsins); // Return the cumulative ASINs with coupons
}

async function main() {
  logMessage('Script started');
  const page = await getAmazon();

  let searchTerm;  // Define searchTerm at the beginning

  try {
    // Check for captcha immediately after launching the page
    let imageUrl = await isCaptcha(page);
    if (imageUrl) {
      await solveCaptcha(page, imageUrl);
    } else {
      logMessage(`No Captcha shown at start.`);
    }

    await zipcodeChange(page);

    searchTerm = await searchTermByUser(page);
    logMessage(`searchTerm received: ${searchTerm}`);


    let hasNextPage = true;
    while (hasNextPage) {
      // Check for captcha before extracting ASINs
      imageUrl = await isCaptcha(page);
      if (imageUrl) {
        await solveCaptcha(page, imageUrl);
      }

      // Extract ASINs after captcha is solved or if no captcha is present
      await extractASINS(page);

      // Check for captcha again before moving to the next page
      imageUrl = await isCaptcha(page);
      if (imageUrl) {
        await solveCaptcha(page, imageUrl);
      }

      hasNextPage = await goNextPage(page);
      if (!hasNextPage) {
        logMessage(`Reached last page.`);
      }
    }
  } catch (error) {
    logMessage(`An error occurred: ${error.message}`);
  } finally {
    if (searchTerm) {  // Check if searchTerm was defined successfully
      await saveAsinsToCSV(searchTerm); // Use searchTerm here
      logMessage('ASINs have been saved (if any were found).');
    } else {
      logMessage('searchTerm was not defined; ASINs were not saved.');
    }
  }

  logMessage('Script finished');
}

main()