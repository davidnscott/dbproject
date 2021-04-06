drop database if exists MealPlanOrganizer;
create database if not exists MealPlanOrganizer;
use MealPlanOrganizer;

create table User(
    /*UserID int not null auto_increment,*/
    FirstName varchar(30),
    LastName varchar(30),
    Age int,
    Gender varchar(15),
    Email varchar(200),
    primary key(Email)
);

create table Instruction(
    InstructionID int not null auto_increment,
    StepNum int,
    Instruction varchar(300),
    primary key(InstructionID)

);



create table Ingredients(
    IngredientID int not null auto_increment,
    IngredientName varchar(50),
    Quantity int,
    Measurement varchar(50),
    primary key(IngredientID)

);

create table Recipe(
    /*MealID varchar(8),*/
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
    /*MealPlanID int,*/
    NameofMeal varchar(30),
    TypeofMeal varchar(30),
    NumofCalories int,
	ImageFileName varchar(50),
    primary key(MealID),
    foreign key (RecID) references Recipe(RecID) on delete cascade on update cascade
	/*Foreign key (MealPlanID) references MealPlan(MealPlanID) on delete cascade on update cascade*/
);

create table MealPlan(
    Email varchar(200),
    #MealID int,
	breakfast varchar(30),
	lucnch varchar(30),
	dinner varchar(30),
    MealPlanID int not null auto_increment,
    #NumofMeals int,
	TotalCalories int,
    DayofWeek varchar(200),
    primary key(MealPlanID),
    foreign key (Email) references User(Email) on delete cascade on update cascade
    #foreign key (MealID) references Meal(MealID) on delete cascade on update cascade

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

