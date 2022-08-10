# Project 2 - Commerce, CS50 Web
#### Video Demo:  <p><https://www.youtube.com/watch?v=uOY-i6mwp4A></p>

![Getting Started](./auctions/static/auctions/img_readme/gettingstarted.gif)

<p align="center">
<img src="https://img.shields.io/badge/release-Jul%2F2022-blue#:~:text=Jul/2022-,Jul/2022"/>
<img src="https://img.shields.io/badge/CS50W-Project 2-blue"/>
<img src="https://img.shields.io/badge/MyOwn-eCommerce-orange"/>
<img src="https://img.shields.io/badge/raphaeuaf-@yahoo.com.br-red"/>
<img src="https://img.shields.io/badge/Pretending-Ebay-yellow"/>
</p>


## Index
* [Title and Logo](#Title-and-Logo)
* [Badges](#badges)
* [Index](#index)
* [Project Description](#project-description)
* [Project Status](#project-status)
* [Application, Features and Requirements](#application-features-and-requirements)
* [Details](#details)
* [Developer](#developer)
* [Conclusion](#conclusion)


## Project Description
<p> The Project 2 of the CS50W is called Commerce. We must complete the implementation of a <b>Auction Site</b>, that is something like <b>ebay</b>, <b>aliexpress</b> or <b>Mercado Livre</b> here in Brazil. The new thing is that we're going to deal with <b>models</b> and <b>databases</b> inside the Django. By the way, this is our second task with Django. It is important to note that this project has a lot of details and, for this reason, it took some weeks to complete.</p>


## Project Status
<p>It was tested a lot. But it always has one or other lacks.</p>


## Application, Features and Requirements
<p>Like the last one, this work was made in <b>Django</b> with a lot of <b>Python</b>, <b>HTML</b> and <b>CSS</b>. The bigger difference, though, it is the use of <b>databases</b>, <b>models</b> and <b>migrations</b>.</p>


## Details
<p>Below, all the details about this project:</p>


### Models
<p><b>Models</b> are the most important subject for this part of the course, so we will have to create some of them. The exercise asks at least three different models: one for <b>auction listings</b> representing the item which will be sold and all of its details, other for <b>bids</b> keeping a kind of history of all offers that will be placed and another for <b>comments</b> with all about that we judge necessary in this field. It's up to us to decide what type of data each model will store so it be worked for us and, maybe, displayed on our e-commerce.</p>
<p>For this project I used five models:</p>

- `1`) <b>User</b>: This model had already been created, but I added the <b>watchlist</b> field in order to store all items that the user wanted to put in this list.
- `2`) <b>Category</b>: This one is to keep all categories with this own field and the <b>quantity</b>, because I wanted to show the number of items from each category.
- `3`) <b>Auction</b>: A different name for <b>listing</b>, but with the same effect. The idea was to keep all important data to a selling product, so I created the fields <b>title</b>, <b>description</b>, <b>start_bid</b>, <b>thereis_bid</b>, <b>current_bid</b>, <b>image_url</b>, <b>is_active</b>, <b>category</b>, <b>owner</b> and <b>date_published</b>.
- `4`) <b>Bid</b>: A model responsible for storing the <b>amount</b> for what <b>auction</b> and the <b>owner</b> that placed the bid.
- `5`) <b>Comment</b>: The last model has the function to collect the <b>auction</b> for which the comment was posted, the <b>content</b>, the <b>author</b> and the <b>date</b> of each comment.

<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/models.gif"/>
</p>


### Create Listing
<p>We should click on <b>Create Listing</b> if we want to put an item to sell. We also should define a <b>title</b> and type some <b>description</b> about our product. After that, we need to set a initial value so the users can place a <b>bid</b>. It's required a <b>URL for an image</b> and choosing one or more <b>categories</b> as well. The <b>seller</b> is automatically pre-fulfilled with the name of the current user.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/create.gif"/>
</p>
<p>All of the fields must be fulfilled. If not, an error message will be displayed to the user:</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/create2.gif"/>
</p>


### Active Listings Page
<p>The default route of the page lets users view all of the auction listings, including those that were closed by the owner without any bid and became <b>unavailable</b> such as those that were closed with one or more bids and were <b>sold</b>. It's up to the owner to delete the <b>unavailable</b> and <b>sold</b> items so that they no longer appear on the main page. Moreover, if we are the owner of an item and we are logged in, the application displays our username preceded by the word "you" throughout the site so that we know which are ours and which are not.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/home.gif"/>
</p>
<p>Notice that we can see for each listing important data such as <b>image</b>, <b>title</b>, <b>description</b>, <b>current price</b>, <b>seller</b> and the <b>date</b> that it was published. Also for each item we see a blue button that allows us <b>view</b> the product and another features and one or more orange buttons indicating which category or categories the sell belongs to. Like the blue button, the orange ones are clickable and, if we do, they take us to the respective category page.</p>


### Listing Page
<p>Clicking on the blue button from any published product, we'll <b>view</b> it in a specific page to that listing. On this page, we can see all details about the listing as well as some features that become available to us, such as adding to or removing from a <b>watchlist</b>, placing <b>bids</b> if the current user is not the owner and the possibility to post comments.</p> 
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/view.gif"/>
</p>
<p>Watchlist, bidding and commenting functionalities is not available to non-logged-in users.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/view_nl.gif"/>
</p>
<p>When we add an item to our watchlist or when we remove it from that, the color of the watchlist button changes and a slighty phrase below the button indicates us of the current situation. A small number meaning the quantity of items from our list appears on the menu bar of the page from this time on.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/add_watchlist.gif"/>
</p>
<p>If the current user is not the owner of an item, bids are allowed. Only one rule is important to <b>place a bid</b>, which is the value being the same or greater than the one displayed for the product. Note that the application identifies the first bid and that it must be at least equal to the starting bid defined by the seller, as well as identifying the other bids and that these must be greater than the previous ones.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/bid.gif"/>
</p>
<p>If the current user is the owner of an item, that is, the user is the one who created the listing, bids are not allowed but two different functions are enabled instead: the seller can close and delete the auction.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/close_wb.gif"/>
</p>
<p>The user who has won the auction can see it on the respective page.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/whowon.gif"/>
</p>
<p>The seller can close the auction without any bids. If it does, the page will display all this information</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/close_nb.gif"/>
</p>
<p>In case the delete button is clicked, a specific page to deleting an item will be opened. In order to avoid mistakes, the password will be required to do this action. If the password is entered correctly, the auction will no longer be displayed.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/del.gif"/>
</p>
<p>Comments are allowed for all logged users on all auctions, whether active or not. They will be shown in descending chronological order.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/comment.gif"/>
</p>


### Watchlist
<p>There is a watchlist page which users can visit. This page displays all items added to it and all ordinary features like the view button, for instance.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/watchlist.gif"/>
</p>


### Categories
<p>We can visit any category directly from the menu that opens when we click on <b>categories</b> button at the top of the page. By clicking on <b>all</b>, a page with all categories will open for us.</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/categories.gif"/>
</p>


### Django Admin Interface
<p> There wasn't much work on this part, as Django has already done almost everything for us. We create a superuser and our models will be available for viewing, adding, editing and deleting. As a superuser, we can add a comment and put the blame on any other user, for example...</p>
<p align="center">
<img style="width: 80%" src="./auctions/static/auctions/img_readme/admin.gif"/>
</p>


## Developer
My name is Raphael Freitas. I'm Brazilian, I'm from Lorena (my city) São Paulo (my state) and my contact is raphaeuaf@yahoo.com.br.


## Conclusion
<p>I want to thank <b>Harvard University / EDX</b> for this oportunity. I am really, really grateful.</p>