# print basic examples:
print("basic print and assignment examples:");
print("string");
print(1);
print(1.23);
x = 5;
print(x);
x += 1;
print(x);

x = 1.2;
print(x);
y = "Luka";
print(y);

# # memory stack example:
print("memory stack example:");
n = 0;
print(n);
{
	n = 1;
	print(n);
	{
		n = 2;
		print(n);
	}
	print(n);
}
print(n);

# matrix ecamples
print("matrix examples:");
y = ones(3);
print(y);
y = eye(3);
print(y);
y = zeros(2, 5);
print(y);
y = ones(2, 5);
print(y);
y = eye(5, 5);
print(y);
y = zeros(3, 5);
print(y);
y[2, 4] = 3;
y[1, 2] = 5;
y[0] = [1, 1, 1, 1, 1];
print(y);

# if example:
print("if example:");
a = 1;
b = 2;
if(a > b)
{
	print("a > b");
}
else
{
	print("a <= b");
}

# while example:
print("while example:");
a = 1;
while(a < 10)
{
	print(a);
	a += 1;
}

# for example:
print("for example:");
a = 1;
b = 9;
for i = a:b
	print(i);
	
# break example:
print("break example:");
a = 1;
while(a < 10)
{
	if(a == 6)
		break;
	print(a);
	a += 1;
}

# continue example:
print("continue example:");
a = 1;
b = 9;
for i = a:b
{
	if(i == 5)
		continue;
	if(i == 6)
		continue;
	print(i);
}	


# # # # some advanced matrix examples? - dotOperations?
# # # # ... TO DO

# some real algorithm example:
print("Real algorithm example: GCD(20, 8) = ");
x = 20;
y = 8;
while(y != 0)
{
	if(x - y > y)
	{
		x = x - y;
	}
	else
	{
		tmp = x;
		x = y;
		y = tmp - y;
	}
}
print(x);
