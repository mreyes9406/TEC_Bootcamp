USE sakila;

# 1a. Display the first and last names of all actors from the table actor.
SELECT 
    first_name, last_name
FROM
    actor;

# 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT 
    UPPER(first_name) AS FIRST_NAME_UPPER,
    UPPER(last_name) AS LAST_NAME_UPPER
FROM
    actor;

# 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
SELECT 
    actor_id, first_name, last_name
FROM
    actor
WHERE
    first_name = 'Joe';

# 2b. Find all actors whose last name contain the letters GEN:
SELECT 
    first_name, last_name
FROM
    actor
WHERE
    last_name LIKE '%gen%';

# 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT 
    first_name, last_name
FROM
    actor
WHERE
    last_name LIKE '%li%'
ORDER BY last_name , first_name;

# 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT 
    country_id, country
FROM
    country
WHERE
    country IN ('Afghanistan' , 'Bangladesh', 'China');

# 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
ALTER TABLE actor
    ADD COLUMN description BLOB;
  
# 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
ALTER TABLE actor
    DROP COLUMN description;

# 4a. List the last names of actors, as well as how many actors have that last name.
SELECT 
    last_name, COUNT(last_name)
FROM
    actor
GROUP BY last_name;

# 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
SELECT 
    last_name, COUNT(last_name)
FROM
    actor
GROUP BY last_name
HAVING COUNT(last_name) >= 2;

# 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
UPDATE actor 
SET 
    first_name = 'HARPO'
WHERE
    first_name = 'GROUCHO'
        AND last_name = 'WILLIAMS';

# 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
UPDATE actor 
SET 
    first_name = 'GROUCHO'
WHERE
    first_name = 'HARPO'
        AND last_name = 'WILLIAMS';

# 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
DESCRIBE actor;

# 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT 
    staff.first_name, staff.last_name, address.address
FROM
    staff
        INNER JOIN
    address ON staff.address_id = address.address_id;

# 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
SELECT 
    staff.first_name,
    staff.last_name,
    SUM(payment.amount)
FROM
    staff
        INNER JOIN
    payment ON payment.staff_id = staff.staff_id
WHERE payment.payment_date BETWEEN '2005-08-01 00:00:00' AND '2005-08-31 23:59:59'
GROUP BY staff.first_name , staff.last_name; 

# 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT 
	film.title, 
    COUNT(film_actor.actor_id) AS number_of_actors
FROM
	film
		INNER JOIN
	film_actor ON film.film_id = film_actor.film_id
GROUP BY film.title;

# 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT 
	film.title,
	COUNT(inventory.film_id) AS copies_in_inventory
FROM
	inventory
		INNER JOIN
	film ON inventory.film_id = film.film_id
WHERE film.title = "HUNCHBACK IMPOSSIBLE";

# 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
SELECT 
    customer.first_name,
    customer.last_name,
    SUM(payment.amount) AS total_paid
FROM
    customer
        INNER JOIN
    payment ON customer.customer_id = payment.customer_id
GROUP BY customer.last_name , customer.first_name;

# 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. 
# Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
SELECT 
    film.title
FROM
    film
        INNER JOIN
    language ON film.language_id = language.language_id
WHERE
    language.name = 'English'
        AND (film.title IN (SELECT 
            title
        FROM
            film
        WHERE
            title LIKE 'K%')
        OR film.title IN (SELECT 
            title
        FROM
            film
        WHERE
            title LIKE 'Q%'));

# 7b. Use subqueries to display all actors who appear in the film Alone Trip.
SELECT 
    actor.first_name, actor.last_name
FROM
    actor
        INNER JOIN
    film_actor ON actor.actor_id = film_actor.actor_id
WHERE
    film_actor.film_id IN (SELECT 
            film_id
        FROM
            film
        WHERE
            title = 'ALONE TRIP');

# 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT 
    customer.first_name, customer.last_name, customer.email
FROM
    customer
        INNER JOIN
    address ON customer.address_id = address.address_id
WHERE
    address.district IN (SELECT 
            address.district
        FROM
            address
                INNER JOIN
            city ON address.city_id = city.city_id
        WHERE
            city.city_id IN (SELECT 
                    city.city_id
                FROM
                    city
                        INNER JOIN
                    country ON city.country_id = country.country_id
                WHERE
                    country.country = 'CANADA'));
                    
# 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
SELECT 
    film.title
FROM
    film
        INNER JOIN
    film_category ON film.film_id = film_category.film_id
WHERE
    film_category.category_id IN (SELECT 
            category_id
        FROM
            category
        WHERE
            name = 'Family');
            
# 7e. Display the most frequently rented movies in descending order.
SELECT 
    film.title, COUNT(sub.film_id)
FROM
    (SELECT 
        film_id
    FROM
        inventory
    INNER JOIN rental ON inventory.inventory_id = rental.inventory_id) AS sub
        INNER JOIN
    film ON film.film_id = sub.film_id
GROUP BY film.title
ORDER BY COUNT(sub.film_id) DESC;

# 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT 
    inventory.store_id, SUM(sub.paid) AS money_brought_in
FROM
    (SELECT 
        rental.inventory_id, payment.amount AS paid
    FROM
        rental
    INNER JOIN payment ON rental.rental_id = payment.rental_id) AS sub
        INNER JOIN
    inventory ON sub.inventory_id = inventory.inventory_id
GROUP BY inventory.store_id;

# 7g. Write a query to display for each store its store ID, city, and country.
SELECT 
    store.store_id, sub.city, sub.country
FROM
    (SELECT 
        A1.address_id AS address_id,
            A1.city AS city,
            country.country AS country
    FROM
        (SELECT 
        address.address_id AS address_id,
            city.city AS city,
            city.country_id AS country_id
    FROM
        address
    INNER JOIN city ON address.city_id = city.city_id) AS A1
    INNER JOIN country ON A1.country_id = country.country_id) AS sub
        INNER JOIN
    store ON sub.address_id = store.address_id;

# 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
SELECT 
    category.name, SUM(revenues.amount) AS gross_revenue
FROM
    category
        INNER JOIN
    film_category AS film_category1 ON film_category1.category_id = category.category_id,
    (SELECT 
        film_category.category_id AS category_id,
            inventory.inventory_id AS inventory_id
    FROM
        film_category
    INNER JOIN inventory ON film_category.film_id = inventory.film_id) AS film_category
        INNER JOIN
    (SELECT 
        rental.inventory_id AS inventory_id,
            payment.amount AS amount
    FROM
        rental
    INNER JOIN payment ON payment.rental_id = rental.rental_id) AS revenues ON film_category.inventory_id = revenues.inventory_id
GROUP BY category.name
ORDER BY SUM(revenues.amount) DESC
LIMIT 5;
	
# 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
# Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW top_5_v AS
    SELECT 
        category.name, SUM(revenues.amount) AS gross_revenue
    FROM
        category
            INNER JOIN
        film_category AS film_category1 ON film_category1.category_id = category.category_id,
        (SELECT 
            film_category.category_id AS category_id,
                inventory.inventory_id AS inventory_id
        FROM
            film_category
        INNER JOIN inventory ON film_category.film_id = inventory.film_id) AS film_category
            INNER JOIN
        (SELECT 
            rental.inventory_id AS inventory_id,
                payment.amount AS amount
        FROM
            rental
        INNER JOIN payment ON payment.rental_id = rental.rental_id) AS revenues ON film_category.inventory_id = revenues.inventory_id
    GROUP BY category.name
    ORDER BY SUM(revenues.amount) DESC
    LIMIT 5;

# 8b. How would you display the view that you created in 8a?
SELECT * FROM top_5_v;

# 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
DROP VIEW IF EXISTS top_5_v;