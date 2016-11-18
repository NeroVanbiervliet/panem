panemApp.service('dictionary', function($rootScope) {

  var dictionary = {};

    // SERVICES
	dictionary.fillServices = function (lang, serviceName) {
		var dic = {};

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
                                "future" : "nog af te halen",
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



    // DIRECTIVES
    dictionary.fillDirectives = function (lang, directiveName) {
		var dic = {};

		switch(lang) {
		    case "en":
						dic = {};
		        break;
		    default: // NL

                switch(directiveName) {
                    case "requestStatusHandler" :
                        dic = {
                            "status" : {
                                "failure" : "Er ging iets fout, herlaad de pagina en probeer opnieuw.",
                                "success" : "Voltooid"
                            }
                        };
                    break;

                    default:
                        dic = {};
                }
		}

		return dic;
	};


    // NAVBAR
    dictionary.fillNavbar = function (lang) {
        var dic = {};

        switch(lang) {
            case "en":
                        dic = {};
                break;
            default: // NL
                    dic = {
                            "login" : "Aanmelden",
                            "register" : "Registeren",
                            "alertMessage" : "Er is een probleem opgetreden, gelieve de pagina te herladen of ons te",
                            "linkToContact" : "contacteren"
                        };
                }

        return dic;
    };


    // CLIENT HOME PAGE
	dictionary.fillClHome = function (lang) {
		var dic = {};

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
                    "searchTitle" : "Zoek uw bakker",
                    "searchPlaceholder" : "Zoek op naam of postcode van de bakkerij",
                    "searchPlaceholderMobile" : "Naam of postcode"
                };
                $rootScope.title = 'Panem - Home';
            }

		return dic;
	};

    // CLIENT MYACCOUNT
    dictionary.fillClMyAccount = function (lang) {
        var dic = {};

        switch(lang) {
            case "en":
                dic = {};
                break;
            default: // NL
                dic = {
                    "creditPanel" : {
                        "currentCredit" : "Huidige krediet",
                        "continue" : "Ga verder",
                        "description" : "Met krediet kunt u snel en eenvoudig bestellingen plaatsen, zonder uw bankkaart te hoeven gebruiken. Klik hieronder om krediet toe te voegen aan uw account.",
                        "added" : "toegevoegd"
                    },
                    "ordersPanel" : {
                        "title" : "Bestellingen",
                        "orderTip" : "Je kunt je bestellingen bekijken en ze opnieuw plaatsen.",
                        "noOrders" : "Bestellingen die je maakt zullen hier getoond worden",
                        "replaceOrder" : "Bestel nog eens",
                        "cancel" : "Annuleren",
                        "confirmCancel" : "Ben je zeker dat je de bestelling wil annuleren?",
                        "yes" : "Ja",
                        "no" : "Nee",
                        "cancelled" : "Geannuleerd"
                    },
                    "cancelFeedback" : {
                      'frozen' : 'De bestelling is al doorgegeven aan de bakker en kan daarom niet meer geannuleerd worden.',
                      'error' : 'Er ging iets fout. Contacteer ons om dit samen op te lossen.'
                    },
                    "changePassword" : "Wachtwoord veranderen"
                };
                $rootScope.title = 'Panem - Mijn account';
            }

        return dic;
    };


  // CLIENT BAKERY PAGE
	dictionary.fillClBakery = function (lang) {
		var dic = {};
		switch(lang) {
		    case "en":
                dic = {};
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
                    "closed" : "gesloten",
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
                    },
                    'overlay' : {
                        'loginMessage' : "Je moet ingelogd zijn om een bestelling te maken.",
                        'btnLogIn' : "Inloggen",
                        'btnRegister' : "Registreren",
                        'noBakerMessage' : "Met een bakkersaccount kun je geen bestellingen plaatsen."
                    },
                    'today' : "Vandaag"
                };
                $rootScope.title = 'Panem - '; // bakery name is added in client/bakery controller
		}

		return dic;
	};


    // CLIENT REGISTER PAGE
	dictionary.fillClRegister = function (lang) {
		var dic = {};

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
                            "alreadyExists" : {
                                'description' : "Er is al een account onder dit email adres. Op deze pagina kun je je wachtwoord resetten.",
                                'toSubstitute' : "deze pagina"
                            },
                            "success" : "Er is een email verstuurd naar"
                    }
                };
                $rootScope.title = 'Panem - Registreer';
		}

		return dic;
	};


    // CLIENT CONTACT AND CONTACT SUCCESS PAGE
	dictionary.fillClContact = function (lang) {
		var dic = {};

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
                            "paymentReference" : "Betalingsreferentie",
                            "question" : "Vraag",
                            "pleaseFillInForm" : "Gelieve alles in te vullen",
                            "send" : "Verstuur",
                            "status" : {
                                "error" : "Er ging iets fout. Herlaadt de pagina en probeer opnieuw.",
                                "success" : "Je vraag werd verzonden"
                            }
                        },
                        'successPage' : {
                            'message' : "Uw bericht werd verstuurd naar onze klantendienst.",
                            'btnHome' : "Naar de homepagina"
                        }
                };
                $rootScope.title = 'Panem - Registreer bakkerij';
          }

		return dic;
	};

// CLIENT CONTACT AND CONTACT SUCCESS PAGE
dictionary.fillClChangePassword = function (lang) {
  var dic = {};

  switch(lang) {
      case "en":
              dic = {};
          break;
    default: // NL
              dic = {
                'form' : {
                  'passwordOld' : "Huidige wachtwoord",
                  'passwordNew' : "Nieuwe wachtwoord",
                  'passwordHelpText' : "Het wachtwoord moet minimaal 7 karakters bevatten",
                  'submit' : "Ga verder"
                },
                'requestStatus' : {
                  'backenderror' : 'Er ging iets fout, gelieve de pagina te herladen en opnieuw te proberen.',
                  'wrongPassword' : 'Het huidige wachtwoord is niet correct.',
                  'reqsNotMet' : 'Het nieuwe wachtwoord voldoet niet aan de voorwaarden.'
                }
              };
              $rootScope.title = 'Panem - Wachtwoord veranderen';
        }

  return dic;
};

    // RESET PASSWORD PAGE
	dictionary.fillClResetPassword = function (lang) {
		var dic = {};

		switch(lang) {
		    case "en":
                dic = {};
		        break;
		    default: // NL
                dic = {
                        "heading" : "Nieuw wachtwoord kiezen",
                        "form" : {
                            "code" : "Code",
                            "codeHelpText" : "De code werd je gestuurd via email.",
                            "password" : "Nieuw wachtwoord",
                            "repeatPassword" : "Herhaal wachtwoord",
                            "passwordHelpText" : "Het wachtwoord moet minimaal 7 karakters bevatten",
                            "submit" : "Ga verder"
                        }
                };
                $rootScope.title = 'Panem - Reset wachtwoord';
		  }

		return dic;
	};


    // FORGOT PASSWORD PAGE
	dictionary.fillClForgotPassword = function (lang) {
		var dic = {};

		switch(lang) {
		    case "en":
                dic = {};
		        break;
		    default: // NL
                dic = {
                    "status" : {
                        "failure" : "Er ging iets fout, herlaad de pagina en probeer opnieuw.",
                        "success" : "Er is een email verstuurd naar"
                    },
                    "heading" : "Wachtwoord vergeten",
                    "fillEmail" : "Vul hieronder je email adres in",
                    "email" : "Email",
                    "continue" : "Verder"
                };
                $rootScope.title = 'Panem - Wachtwoord vergeten';
		}

		return dic;
	};


    // CLIENT LOGIN PAGE
	dictionary.fillClLogin = function (lang) {
		var dic = {};

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
                    'forgotPassword' : "Ik ben mijn wachtwoord vergeten.",
                    "requestStatus" : {
                            "backenderror" : "Er ging iets fout, herlaad de pagina en probeer opnieuw.",
                            "wrongpassword" : "Het wachtwoord klopt niet",
                            "accnotfound" : "Het gegeven emailadres werd niet gevonden",
                            "success" : "U bent nu ingelogd."
                        }
                };
                $rootScope.title = 'Panem - Inloggen';
		}

		return dic;
	};


    // CLIENT CONFIRM ORDER PAGE
    dictionary.fillClConfirmOrder = function (lang) {
        var dic = {};

        switch(lang) {
            case "en":
                dic = {};
                break;
            default: // NL
                dic = {
                    "backToEditOrder" : "De bestelling verder bijwerken",
                    "panelTitle" : "Overzicht van de bestelling",
                    "pickUpOn" : "afhalen op",
                    "tableHeading" : {
                        "product" : "product",
                        "amount" : "aantal stuks",
                        "price" : "prijs per eenheid (€)"
                    },
                    "total" : "Totaal",
                    "credit" : "Krediet",
                    "toPay" : "Resterend te betalen",
                    "insufficientFunds" : "Je hebt onvoldoende krediet. Om de bestelling te plaatsen kun je doorgaan met online betalen.",
                    "payWithCredits" : "Betaal met krediet",
                    "addCreditToAccount" : "Voeg ook krediet toe aan mijn account",
                    "addCreditToAccountTooltip" : "Krediet kun je later gebruiken om een andere online bestelling te plaatsen zonder opnieuw je bankgegevens te hoeven gebruiken",
                    "bonusCredit" : "Vanaf 10 euro krijg je twee euro extra krediet!",
                    "payOnline" : "Betaal",
                    "looksGreat" : "Ik denk dat de bestelling klopt",
                    "paymentIsSecure" : "De betaling wordt veilig verwerkt door onze partner Adyen",
                    "promoCode" : "Promotie code",
                    "promoFeedback" : {
                        'valid' : "geldige code",
                        'notfound' : "ongeldige code",
                        'used' : "is al gebruikt"
                    },
                    'promoExplanation' : "Een code geeft je recht op twee euro gratis krediet, bij het opladen van minstens tien euro"
                };
                $rootScope.title = 'Panem - Bevestig bestelling';
        }

        return dic;
    };

    // CLIENT VERIFY REGISTER PAGE
    dictionary.fillClVerifyAccount = function (lang) {
        var dic = {};

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
                        "heading" : "Foute gegevens",
                        "description" : "We kunnen uw account niet bevestigen. Gelieve contact op te nemen met onze hulpdienst.",
                        "toSubstitute" : "hulpdienst"
                    },
                    "backendRequestFail" : {
                        "heading" : "Oeps, er ging iets fout",
                        "description" : "Probeer de pagina eens opnieuw te laden"
                    }
                };
                $rootScope.title = 'Panem - Verifieer registratie';
        }

        return dic;
    };


    // BAKER REGISTER PAGE
	dictionary.fillBkRegister = function (lang) {
		var dic = {};

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
                        'address' : {
                          'street' : 'Straat',
                          'postcode' : 'Postcode',
                          'city' : 'Stad'
                        },
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
                    },
                    'status' : {
                        'failure' : "Er ging iets fout, herlaad de pagina en probeer opnieuw.",
                        'success' : "De bakkerij werd aangemaakt. Gelieve de email te lezen die we je toegestuurd hebben.",
                        'bakeryalreadyexists' : "Deze bakkerij bestaat al. Indien je dit niet zelf gedaan hebt, gelieve dan contact op te nemen met ons.",
                        'accountalreadyexists' : "Dit email adres is al in gebruik."
                    }
                };
                $rootScope.title = 'Panem - Registreer bakkerij';
		}

		return dic;
	};


    // BAKER DAY ORDER PAGE
	dictionary.fillBkDayOrder = function (lang) {
		var dic = {};

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
                $rootScope.title = 'Panem - Bestelling van een dag';
		}

		return dic;
	};

    // BAKER MODIFYPRODUCTS PAGE
	dictionary.fillBkModifyProducts = function (lang) {
		var dic = {};

		switch(lang) {
		    case "en":
                dic = {};
		        break;
		    default: // NL
                dic = {
                    "introduction" : {
                        "introText" : "Op deze pagina kun je je bakkerij beheren.",
                        "buttonText" : "Naar de klantenpagina",
                    },
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
                    "to" : "tot",
                    "status" : {
                        "success" : "Je wijzigingen werden opgeslagen",
                        "failure" : "Er ging iets fout"
                    }
                };
                $rootScope.title = 'Panem - Beheer producten';
		}

		return dic;
	};


    // BAKER ALL ORDERS PAGE
	dictionary.fillBkAllOrders = function (lang) {
		var dic = {};

		switch(lang) {
		    case "en":
                dic = {};
		        break;
		    default: // NL
                dic = {
                    "IETF" : "nl-BE",
                    "panelTitle" : "Totale bestellingen per dag",
                    "panelDescription" : "Hieronder zijn alle bestellingen weergegeven per dag. Klik op een bestelling voor meer informatie",
                    "noOrders" : "Er zijn er nog geen bestellingen geplaatst. Bestellingen die gemaakt worden zullen hier getoond worden",
                    "tableHead" : {
                        "date" : "Datum",
                        "totalOrders" : "Totaal aantal bestellingen",
                        "totalPrice" : "Totaal bedrag",
                    },
                    "nextDays" : ["vandaag","morgen","overmorgen"]
                };
                $rootScope.title = 'Panem - Alle bestellingen';
		}

		return dic;
	};

    // BAKER MANAGE BAKERY PAGE
	dictionary.fillBkManageBakery = function (lang) {
		var dic = {};

		switch(lang) {
		    case "en":
                dic = {};
		        break;
		    default: // NL
                dic = {
                    'heading' : {
                        'title' : "Beheer je bakkerij",
                        'description' : "Op deze pagina kun je je bakkerij beheren. Als je hulp nodig hebt, contacteer ons dan hier."
                    },
                    'orders' : {
                        'title' : "Bestellingen",
                        'nextOrder' : "Bestelling voor morgen",
                        'amount' : "Aantal bestellingen",
                        'money' : "Totaal bedrag",
                        'details' : "Details",
                        'allOrders' : "Overzicht van alle bestellingen"
                    },
                    'modify' : {
                        'title' : "Aanbod, openingsuren en tijdstip van laatste bestelling",
                        'currentBakeryPage' : "Om te zien hoe je bakkerij er op dit moment uit ziet voor je klanten, ga dan naar je online winkel. Als je dit wil aanpassen, ga dan naar de beheerspagina.",
                        'toClientBakery' : "Naar mijn online winkel",
                        'toModifyPage' : "Naar de beheerspagina"
                    },
                    'notifications' : {
                        'title' : "Email meldingen",
                        'destinationEmail' : "Meldingen worden gestuurd naar",
                        'toggles' : {
                            'nextDayOrder' : "Stuur me een email wanneer de bestelling voor de volgende dag compleet is"
                        }

                    },
                    "status" : {
                        "failure" : "Er ging iets fout, herlaad de pagina en probeer opnieuw.",
                        "success" : "Voorkeuren zijn opgeslagen."
                    }
                };
                $rootScope.title = 'Panem - Beheer bakkerij';
		}

		return dic;
	};

    // CLIENT FINALISE PAYMENT PAGE
	dictionary.fillClFinalisePayment = function (lang) {
		var dic = {};

		switch(lang) {
		    case "en":
                dic = {};
		        break;
		    default: // NL
                dic = {
                    'judgment' : {
                        'cancelled' : {
                            'title' : "De betaling werd geanulleerd",
                            'description' : "De betaling werd door u geanulleerd."
                        },
                        'refusedAdyen' : {
                            'title' : "De betaling werd geweigerd.",
                            'description' : "De betaling werd geweigerd door onze partner. Een medewerker van Panem is automatisch op de hoogte gebracht. U wordt binnenkort gecontacteerd."
                        },
                        'refusedPanem' : {
                            'title' : "De betaling werd geweigerd",
                            'description' : "De betaling werd geweigerd. Wellicht heeft u onvoldoende krediet."
                        },
                        'pending' : {
                            'title' : "De betaling wordt nog verwerkt",
                            'description' : "De betaling is nog niet volledig verwerkt. Een medewerker van Panem is automatisch op de hoogte gebracht. U wordt binnenkort gecontacteerd."
                        },
                        'adyenerror' : {
                            'title' : "Er is iets fout gegaan met de betaling bij adyen",
                            'description' : "Een medewerker van Panem is automatisch op de hoogte gebracht. U wordt binnenkort gecontacteerd."
                        },
                        'backenderror' : {
                            'title' : "Intern probleem",
                            'description' : "Er trad een probleem op. Gelieve de pagina te herladen door op de knop hieronder te klikken.",
                            'buttonText' : 'Herlaad'
                        },
                        'success' : {
                            'title' : "Betaling aanvaard"
                        },
                        'nocurrentorder' : {
                            'title' : "Er is geen betaling af te handelen",
                            'description' : "Waarschijnlijk ben je hier per ongeluk terecht gekomen"
                        },
                        'topUpSuccess' : {
                            'title' : "Betaling aanvaard",
                            'description' : "Uw krediet werd aangevuld."
                        }
                    },
                    'toHome' : {
                        'baseText' : "Klik hier om naar de homepagina te gaan",
                        'toSubstitute' : 'hier'
                    },
                    'questions' : {
                        'title' : "Een vraag over je betaling?",
                        'baseText' : "Als je vragen hebt over deze betaling, gelieve dan contact op te nemen met vermelding van het betalingsnummer : ",
                        'toSubstitute' : 'contact'
                    }
                };
                $rootScope.title = 'Panem - Betaling controleren';
		}

		return dic;
	};

    // CLIENT TOP UP CREDIT PAGE
	dictionary.fillClTopUpCredit = function (lang) {
		var dic = {};

		switch(lang) {
		    case "en":
                dic = {};
		        break;
		    default: // NL
                dic = {
                    "panelTitle" : "Voeg krediet toe aan account",
                    "addCreditToAccount" : "Krediet toevoegen aan je account",
                    "addCreditToAccountTooltip" : "Krediet kun je later gebruiken om een andere online bestelling te plaatsen zonder opnieuw je bankgegevens te hoeven gebruiken",
                    "payOnline" : "Voeg krediet toe",
                    "paymentIsSecure" : "De betaling wordt veilig verwerkt door onze partner Adyen",
                    "promoCode" : "Promotie code",
                    "promoFeedback" : {
                        'valid' : "geldige code",
                        'notfound' : "ongeldige code",
                        'used' : "is al gebruikt"
                    },
                    'promoExplanation' : "Een code geeft je recht op twee euro gratis krediet, bij het opladen van minstens tien euro"
                };
                $rootScope.title = 'Panem - Krediet opladen';
		}

		return dic;
	};

	return dictionary;
});
