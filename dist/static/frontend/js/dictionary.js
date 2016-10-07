panemApp.service('dictionary', function() {
   
  var dictionary = {};

  //////////////
  // SERVICES //
  //////////////  
	dictionary.fillServices = function (lang, serviceName) {
		var dic = {}

		switch(lang) {
		    case "en":
						dic = {};
		        break;
		    default: // NL
				
                switch(serviceName) {
                    case "processDate" : 
                        dic = {
                            "nextDayNames" : {
                                "-1" : "gisteren",
                                "0" : "vandaag",
                                "1" : "morgen",
                                "2" : "overmorgen"
                            },
                            "IETF" : "nl-BE",
                            "qualitativePastTime" : {
                                "0" : "vandaag",
                                "1" : "gisteren",
                                "2" : "eergisteren",
                                "3" : "drie dagen geleden",
                                "4" : "vier dagen geleden",
                                "5" : "vijf dagen geleden",
                                "6" : "zes dagen geleden",
                                "7" : "een week geleden",
                                "8" : "meer dan een week geleden",
                                "14": "twee weken geleden",
                                "21": "drie weken geleden",
                                "31": "een maand geleden",
                                "62": "twee maanden geleden",
                                "93": "drie maanden geleden",
                                "124": "vier maanden geleden",
                                "155": "vijf maanden geleden",
                                "186": "een half jaar geleden",
                                "365": "meer dan een jaar geleden"
                                }
                        };
                    break; 
                        
                    default: 
                        dic = {}; 
                }
		}

		return dic;
	};
    
    
    
  //////////////
  // SERVICES //
  //////////////  
    dictionary.fillNavbar = function (lang) {
        var dic = {}

        switch(lang) {
            case "en":
                        dic = {};
                break;
            default: // NL
                    dic = {
                            "login" : "Aanmelden",
                            "register" : "Registeren"
                        }
                };

        return dic;
    };
    
    
  //////////////////////
  // CLIENT HOME PAGE //
  //////////////////////  
	dictionary.fillClHome = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
						dic = {
				        "title" : "Panem",
				        "slogan" : "Order bread online",
				        "search" : "Search bakery by name or postal code"
				    };
		        break;
		    default: // NL
						dic = {
                        "title" : "Panem",
				        "searchTitle" : "Zoek uw bakker",
				        "searchPlaceholder" : "Zoek op naam of postcode van de bakkerij"
				    };
		}

		return dic;
	};
    
  //////////////////////
  // CLIENT MYACCOUNT //
  //////////////////////  
    dictionary.fillClMyAccount = function (lang) {
        var dic = {}

        switch(lang) {
            case "en":
                        dic = {};
                break;
            default: // NL
                        dic = {
                            "creditPanel" : {
                                "currentCredit" : "Huidige krediet",
                                "continue" : "Ga verder",
                                "description" : "Met krediet kunt u snel en eenvoudig bestellingen plaatsen, zonder uw bankkaart te hoeven gebruiken. Klik hieronder om krediet toe te voegen aan uw account."
                            },
                            "ordersPanel" : {
                                "title" : "Bestellingen"
                            }
                    };
        }

        return dic;
    };


  ////////////////////////
  // CLIENT BAKERY PAGE //
  ////////////////////////
	dictionary.fillClBakery = function (lang) {
		var dic = {}
		switch(lang) {
		    case "en":
						dic = {
				        "title" : "Panem",
				        "slogan" : "Order bread online",
				        "search" : "Search bakery by name or postal code"
				    };
		        break;
		    default: // NL
						dic = {
                            "IETF" : "nl-BE",
							"bakeryDescription" : {
                                "openingHours" : "openingsuren",
                                "noOpeningHours" : "Geen gegevens beschikbaar",
                                "noProducts" : "Deze bakker heeft nog geen producten toegevoegd"
                            },
                            "orderLabels" : {
                                "order" : "Bestelling",
                                "remarks" : "Opmerkingen",
                                "pickupDate" : "Afhaaldatum",
                                "previousOrders" : "Eerdere bestellingen",
                                "currentOrder" : "Huidige bestelling",
                                "bakeryIsClosed" : "De bakker is deze dag gesloten",
                                "continue" : "Ga verder"
                            },
                            "nextDays" : ["vandaag","morgen","overmorgen"],
                            "weekDays" : ["zondag","maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag"],
                            "weekDaysNew" : ["maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag","zondag"],
                            "hourAbbr" : "u",
                            "qualitativePastTime" : {
                                "1" : "gisteren",
                                "2" : "eergisteren",
                                "3" : "drie dagen geleden",
                                "4" : "vier dagen geleden",
                                "5" : "vijf dagen geleden",
                                "7" : "een week geleden",
                                "14": "twee weken geleden",
                                "21": "drie weken geleden",
                                "31": "een maand geleden",
                                "62": "twee maanden geleden",
                                "93": "drie maanden geleden",
                                "124": "vier maanden geleden",
                                "155": "vijf maanden geleden",
                                "186": "een half jaar geleden",
                                "365": "meer dan een jaar geleden"
                                }
				        };
		}

		return dic;
	};


  //////////////////////////
  // CLIENT REGISTER PAGE //
  //////////////////////////
	dictionary.fillClRegister = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
				    dic = {
				        "title" : "Panem - register",
				        "formDescription" : "Click here to register your bakery with panem"
    				};
		        break;
		    default: // NL
				    dic = {
				        "title" : "Panem - registreer",
				        "form" :  {
                            "firstName" : "Voornaam",
                            "lastName" : "Achternaam",
                            "emailAdress" : "Email adres",
                            "repeatEmail" : "Herhaal email",
                            "password" : "Wachtwoord",
                            "repeatPassword" : "Herhaal wachtwoord",
                            "adress" : "Adres",
                            "adressPlaceholder" : "Straat, postcode en stad",
                            "checkbox" : {
                                "iHave" : "Ik heb de ",
                                "termsAndConditions" : "algemene voorwaarden ",
                                "readAndConsent" : "gelezen en goedgekeurd."
                            },
                            "passwordHelpText" : "Het wachtwoord moet minimaal 7 karakters bevatten",
                            "submit" : "Ga verder"
                        },
                        "requestStatus" : {
                                "inProgress" : "Uw gegevens worden verwerkt, even geduld.",
                                "backendError" : "Er ging iets fout, herlaad de pagina en probeer opnieuw.",
                                "alreadyExists" : "Er is al een account onder dit email adres. NEED link naar reset account page",
                                "success" : "Er is een email verstuurd naar"
                        }
    				};
		}

		return dic;
	};

    /////////////////////////
    // CLIENT CONtACT PAGE //
    /////////////////////////
	dictionary.fillClContact = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
				    dic = {};
		        break;
		    default: // NL
				    dic = {
                            "heading" : "Kies hoe je ons contacteert",
                            "viaTelephone" : "Telefonisch",
                            "viaEmail" : "Per email",
                            "form" : {
                                "viaForm" : "Via dit formulier",
                                "name" : "Naam",
                                "email" : "Email",
                                "telephone" : "Telefoon",
                                "question" : "Vraag",
                                "pleaseFillInForm" : "Gelieve alles in te vullen",
                                "send" : "Verstuur",
                                "status" : {
                                    "error" : "Er ging iets fout. Herlaadt de pagina en probeer opnieuw.",
                                    "success" : "Je vraag werd verzonden"
                                }
                            }
    				};
		}

		return dic;
	};
    
    ///////////////////////
    // CLIENT LOGIN PAGE //
    ///////////////////////
	dictionary.fillClLogin = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
				    dic = {
				        "title" : "Panem - register",
				        "formDescription" : "Click here to register your bakery with panem"
    				};
		        break;
		    default: // NL
				    dic = {
                        "form" : {
                            "emailAdress" : "Email",
                            "password" : "Wachtwoord",
                            "submit" : "Verder"
                        },
                        "requestStatus" : {
                                "backenderror" : "Er ging iets fout, herlaad de pagina en probeer opnieuw.",
                                "wrongpassword" : "Het wachtwoord klopt niet",
                                "accnotfound" : "Het gegeven emailadres werd niet gevonden",
                                "success" : "U bent nu ingelogd."
                            }
    				};
		}

		return dic;
	};
    
    ///////////////////////////////
    // CLIENT CONFIRM ORDER PAGE //
    ///////////////////////////////
    dictionary.fillClConfirmOrder = function (lang) {
        var dic = {}

        switch(lang) {
            case "en":
                    dic = {
                        "title" : "Panem - register",
                        "formDescription" : "Click here to register your bakery with panem"
                    };
                break;
            default: // NL
                    dic = {
                        "backToEditOrder" : "De bestelling verder bijwerken",
                        "panelTitle" : "Overzicht van de bestelling",
                        "tableHeading" : {
                            "product" : "product",
                            "amount" : "aantal stuks",
                            "price" : "prijs per eenheid (€)"
                        },
                        "total" : "Totaal",
                        "credit" : "Krediet",
                        "toPay" : "Resterend te betalen",
                        "payWithCredits" : "Betaal met krediet",
                        "addCreditToAccount" : "Voeg krediet toe aan mijn account",
                        "bonusCredit" : "Vanaf 10 euro krijg je twee euro extra krediet!",
                        "payOnline" : "Betaal online",
                        "paymentIsSecure" : "De betaling wordt veilig verwerkt door onze partner Adyen"
                    };
        }

        return dic;
    };
    
    //////////////////////////////////
    // CLIENT CONFIRM REGISTER PAGE //
    //////////////////////////////////
    dictionary.fillClConfirmRegister = function (lang) {
        var dic = {}

        switch(lang) {
            case "en":
                    dic = {
                        "title" : "Panem - register",
                        "formDescription" : "Click here to register your bakery with panem"
                    };
                break;
            default: // NL
                    dic = {
                        "confirmed" : {
                            "heading" : "Email is bevestigd",
                            "description" : "U kunt nu aan de slag met Panem! Klik op de knop hieronder om naar de homepagina te gaan. Daar kunt u uw bakker zoeken en een bestelling plaatsen.",
                            "buttonText" : "Naar Home"
                        },
                        "wasAlreadyConfirmed" : {
                            "heading" : "Email was al bevestigd",
                            "description" : "Uw email adres was al bevestigd."
                        },
                        "noCorrectCodeOrEmail" : {
                            "heading" : "Foute gegevens"
                        },
                        "backendRequestFail" : {
                            "heading" : "Oeps, er ging iets fout",
                            "description" : "Probeer de pagina eens opnieuw te laden"
                        }
                    };
        }

        return dic;
    };
    
  /////////////////////////
  // BAKER REGISTER PAGE //
  /////////////////////////
	dictionary.fillBkRegister = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
				    dic = {};
		        break;
		    default: // NL
				    dic = {
                        "personalInfo" : {
                            "title" : 'Persoonlijke gegevens',
                            'firstName' : 'Voornaam',
                            'lastName' : 'Achternaam',
                            'email' : 'Emailadres',
                            'emailTooltip' : 'Persoonlijk emailadres voor communicatie met panem',
                            "password" : "Wachtwoord",
                            "passwordTooltip" : "Dit zul je gebruiken om in te loggen op deze website. Vereisten: NEED"
                        },
                        "bakeryInfo" : {
                            'title' : 'Gegevens over de bakkerij',
                            'name' : 'Naam bakkerij',
                            'adress' : 'Adres',
                            'telephone' : 'Telefoonnummer',
                            'taxNumber' : 'BTW-nummer',
                            'bankAccount' : 'Rekeningnummer',
                            'bankAccountTooltip' : 'Panem stort de aankopen die via deze website worden betaald naar dit rekeningnummer door',
                            'bankAccountPlaceholder' : 'bv. BE46 0016 1525 7336',
                        },
                        'submitText' : 'Ga verder',
                        "checkbox" : {
                                "iHave" : "Ik heb de ",
                                "termsAndConditions" : "algemene voorwaarden ",
                                "readAndConsent" : "gelezen en goedgekeurd."
                        }
				    };
		}

		return dic;
	};

  //////////////////////////
  // BAKER DAY ORDER PAGE //
  //////////////////////////
	dictionary.fillBkDayOrder = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
				    dic = {};
		        break;
		    default: // NL
				    dic = {
                        "IETF" : "nl-BE",
                        "aggregatePanel" : {
                            "title" : "Overzicht bestellingen voor",
                            "totalNumberOfOrders" : "Totaal aantal bestellingen", 
                            "totalMoney" : "Totaal bedrag van de bestellingen",
                            "print" : "Afdrukken"
                        },
                        "individualPanel" : {
                            "title" : "Bestellingen per persoon",
                            "remarks" : "Opmerkingen",
                            "payed" : "online betaald",
                            "notpayed" : "niet betaald"
                        },
                        "nextDays" : ["vandaag","morgen","overmorgen"],
                    };
		}

		return dic;
	};

    ///////////////////////////////
    // BAKER MODIFYPRODUCTS PAGE //
    ///////////////////////////////
	dictionary.fillBkModifyProducts = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
				    dic = {};
		        break;
		    default: // NL
				    dic = {
                        "panelTitles" : {
                            "products" : "Producten",
                            "openingHours" : "Openingsuren",
                            "lastOrderHour" : "Limiet bestelling voor volgende dag"
                        },
                        "category" : "Categorie",
                        "addCustomProduct" : "Voeg een eigen product toe",
                        "productNamePlaceholder" : "Naam product",
                        "ingredientsPlaceholder" : "ingrediënten",
                        "saveChanges" : "Wijzigingen bewaren",
                        "daysOfTheWeek" : [{"name" : "maandag"},{"name" : "dinsdag"},{"name" : "woensdag"},{"name" : "donderdag"},{"name" : "vrijdag"},{"name" : "zaterdag"},{"name" : "zondag"}],
                        "from" : "van",
                        "to" : "tot"
                            };
		}

		return dic;
	};
    
    
  ///////////////////////////
  // BAKER ALL ORDERS PAGE //
  ///////////////////////////
	dictionary.fillBkAllOrders = function (lang) {
		var dic = {}

		switch(lang) {
		    case "en":
				    dic = {};
		        break;
		    default: // NL
				    dic = {
                        "IETF" : "nl-BE",
                        "panelTitle" : "Totale bestellingen per dag",
                        "panelDescription" : "Hieronder zijn alle bestellingen weergegeven per dag. Klik op een bestelling voor meer informatie",
                        "tableHead" : {
                            "date" : "Datum",
                            "totalOrders" : "Totaal aantal bestellingen",
                            "totalPrice" : "Totaal bedrag",
                        },
                        "nextDays" : ["vandaag","morgen","overmorgen"]
                    };
		}

		return dic;
	};

	return dictionary;
});