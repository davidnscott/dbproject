/*drop database if exists MealPlanOrganizer;
create database if not exists MealPlanOrganizer;
use MealPlanOrganizer;

create table User(
    FirstName varchar(30),
    LastName varchar(30),
    Age int,
    Gender varchar(15),
    Email varchar(200),
    primary key(Email)
);

create table Instruction(
    InstructionID int not null auto_increment,
    Step1 varchar(200),
    Step2 varchar(200),
	Step3 varchar(200),
    primary key(InstructionID)

);



create table Ingredients(
    IngredientID int not null auto_increment,
    IngredientName varchar(50),
    Measurement varchar(50),
    primary key(IngredientID)

);

create table Recipe(
    RecID int not null auto_increment,
    InstructionID int,
    IngredientID int,
    CreationDate date,
    RDescription varchar(300),
    TypeofDiet varchar(20),
    Servings int,
    primary key(RecID),
    foreign key (IngredientID) references Ingredients(IngredientID) on delete cascade on update cascade,
    foreign key (InstructionID) references Instruction(InstructionID) on delete cascade on update cascade
);

create table Meal(
    MealID int not null auto_increment,
    RecID int,
    NameofMeal varchar(30),
    TypeofMeal varchar(30),
    NumofCalories int,
	ImageFileName varchar(50),
    primary key(MealID),
    foreign key (RecID) references Recipe(RecID) on delete cascade on update cascade
);

create table MealPlan(
    Email varchar(200),
	breakfast varchar(30),
	lunch varchar(30),
	dinner varchar(30),
    MealPlanID int not null auto_increment,
	TotalCalories int,
    DayofWeek varchar(200),
    primary key(MealPlanID),
    foreign key (Email) references User(Email) on delete cascade on update cascade

);

create table Kitchen(
    Email varchar(200),
    KitchenID int not null auto_increment,
    IngredientID int,
    Primary key(KitchenID),
    foreign key (Email) references User(Email) on delete cascade on update cascade,
    Foreign key (IngredientID) references Ingredients(IngredientID) on delete cascade on update cascade
);

create table Shopping_List(
    SLID int not null auto_increment,
    KitchenID int,
    IngredientID int,
    Primary key(SLID),
    Foreign key (KitchenID) references Kitchen(KitchenID) on delete cascade on update cascade,
    Foreign key (IngredientID) references Ingredients(IngredientID) on delete cascade on update cascade

);

DELIMITER //
create procedure generate_shopping_list (in email varchar(200))
begin
select distinct(IngredientName) from Recipe natural join ingredients where IngredientID not in (select IngredientID from Kitchen) and IngredientID in (select IngredientID from mealplan natural join meal natural join recipe where email = email);
END //
DELIMITER ;
*/
DELIMITER //
create procedure recipe_display (in id varchar(200))
begin
Select recid,RDescription,creationdate,typeofdiet,step1,step2,step3,ingredientname,measurement from Recipe natural join ingredients natural join instruction where recid = id;
END //
DELIMITER ;


