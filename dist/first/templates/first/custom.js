// is executed on loading of the page
window.onload = function() {
    // fill the content of the tabs
    fillTabContent();
};

// fills the page according to the current bakery supply
function fillTabContent() {
    
    // default image if none is provided
    var defaultImage = "url(http://i.imgur.com/QkeLA4h.jpg)"; // TODO aanpassen
    
    // create standard element to display a product. this will later be cloned many times
    var plusSpan = document.createElement('span');
    plusSpan.className = "plus";
    plusSpan.innerHTML = "+";
    
    var overlayDiv = document.createElement('div');
    overlayDiv.className = "overlay";
    overlayDiv.appendChild(plusSpan);
    
    var boxDiv = document.createElement('div');
    boxDiv.className = "box";
    boxDiv.style.backgroundImage = defaultImage;
    boxDiv.appendChild(overlayDiv); 
    
    var colDiv = document.createElement('div');
    colDiv.className = "col-md-1 colPad";
    colDiv.appendChild(boxDiv);
    
    var pName = document.createElement('p');
    pName.className = "text-center"; // TODO centering gebeurt precies enkel als je scherm verkleint
    var pPrice = document.createElement('p'); // TODO other formatting for price
    pPrice.className = "text-center"; 
    colDiv.appendChild(pName);
    colDiv.appendChild(pPrice);
    
    // create standard tab item
    var tabA = document.createElement('a');
    tabA.setAttribute("data-toggle","tab");
    var tabLi = document.createElement('li'); 
    tabLi.appendChild(tabA);
    
    // create standard tabContent item
    var tabContentDiv = document.createElement('div');
    tabContentDiv.className = "tab-pane fade"; 
    
    // dummy data TODO remove
    var product1 = {
        "name" : 'croissant',
        "price" : 1.4,
        "photoUrl" : 'images/croissant.jpg'
    };
    var product2 = {
        "name" : 'chocoladekoek',
        "price" : 1.5,
        "photoUrl" : 'images/chocoladekoek.jpg'
    };
    var product3 = {
        "name" : 'achtkoek',
        "price" : 1.5,
        "photoUrl" : 'images/achtkoek.jpg'
    };

    var cat1 = {
            "name" : 'Broden',
            "products" : [product1]
        };
    var cat2 = {
            "name" : 'Koffiekoeken',
            "products" : [product1, product2, product3,product3]
        };
    var cat3 = {
            "name" : 'Klein gebak',
            "products" : [product3]
        };
    var cat4 = {
            "name" : 'Taarten',
            "products" : [product3]
        };
    var cat5 = {
            "name" : 'Pistolets & Broodjes',
            "products" : [product3]
        };
    var categories = [cat1, cat2, cat3, cat4, cat5];

    
    // store the tab control elements
    var tabsList = document.getElementById("tabsList");
    var tabsContent = document.getElementById("tabsContent");
    
    var iLength = categories.length;
    for (var i = 0; i < iLength; i++) 
    {
        // get the current category name
        var catName = categories[i].name; 
        
        // create new tab li
        var newTabLi = tabLi.cloneNode(true);
        
        // edit id and text
        var strippedName = catName.replace(/\W/g, '');
        strippedName = strippedName.replace(' ',''); // remove spaces TODO nog nodig? 
        var tabContentId = "content".concat(strippedName);
        newTabLi.firstChild.href = "#".concat(tabContentId);
        newTabLi.firstChild.innerHTML = catName; 
        
        // add the li to the tabs, but add it just before the last child of tabList (being the search bar)
        tabsList.insertBefore(newTabLi, tabsList.lastChild); // TODO werkt niet, searchbar blijft niet rechts
        
        // create a tab to contain the content
        newTabContentDiv = tabContentDiv.cloneNode(true); 
        newTabContentDiv.id = tabContentId;         
        
        // add to the tabContent
        tabsContent.appendChild(newTabContentDiv);
        
        if(i==0) // first tab 
        {
            newTabLi.className = "active"; // dit wordt de active tab bij laden
            newTabContentDiv.className = newTabContentDiv.className.concat(" in active");
        }
        
        // TODO er moet eerst nog een row voor er een column komt in de tabs!! en steek er ook spacer als klasse bij om plek te geven
        
        // loop over all products in category
        var products = categories[i].products; 
        var jLength = products.length; 
        
        for (var j = 0; j < jLength; j++) 
        {
            var product = products[j];
            
            var newProduct = colDiv.cloneNode(true);
            
            // add product info to sterile clone
            newProduct.firstChild.style.backgroundImage = "url(".concat(product.photoUrl).concat(")");
            newProduct.children[1].innerHTML = product.name;
            newProduct.children[2].innerHTML = product.price; 
            
            newTabContentDiv.appendChild(newProduct);
            
            // TODO indien te veel elementen overflow naar volgende row
        }
    }    
}