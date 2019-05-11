# assignments:
x = 0;
x -= 0.5;
x += "a";		#error
y += 5.5;		#error
y = 5.5;
z -= "asdf";	#error
z = "Stu";
z += "dent";

# assignments with scopes:
{
	x -= 1;
	{
		y *= 5;
		n = 0;
		{
			n -= 1;
			m = "Some";
			m += "thing";
		}
		n += 1;
		m += "wrong";		#error
	}
	n -= 0;					#error
}

# matrixes - initlialization:
A = [1, 2, 3];							#type: matrix3
B = [[1, 2, 3], [4, 5, 6]];				#type: matrix2x3	
C = [[[1, 2, 3, 4], [5, 6, 7, 8]], [[9, 10, 11, 12], [13, 14, 15, 16]], [[17, 18, 19, 20], [21, 22, 23, 24]]]; 	#type: matrix3x2x4
E = [1, "some string"];		#error
F = [[1, 2], [1, 2, 3]];	#error
G = [						#error
	 [1,2,3],
     [1,2,3,4,5],
     [1,2]
    ];
# # matrixes - wrong indexes:
A[0] = 1;
A[0, 1] = 0;	#error
A[3] = 1;		#error
B[1, 2] = 1;
B[2, 2] = 0;	#error
B[1, 3] = 0;	#error
B[0, 0, 0, 0, 0] = 0;	#error
C[2, 1, 3] = 0;
C[0, 1] = [1, 2, 3, 4];
C[3, 3, 3] = 0;	#error
C[0, 0, 4] = 0;	#error
# # matrixes - wrong types:
A[0] = "string";	#error
A[0] = 1.0;			#error
C[0, 0, 0] = 0.0;	#error
C[0, 0, 0] = "string";	#error	
B[1, 2] = 0.9;	#error
C[0, 1] = [1, 2];		#error
C[0, 1] = [1.0, 2.0, 3.0, 4.0];	#error


# for:
for i = 1:N {
    for j = i:M {
        print i, j;
    }
}

# binexpr:
x = 0.0;
y = "string";
z = x + y;

#condition:
if(x > y){
	x -= 0.0;
}

# matrix operation:
A = [[0, 1], [2, 3]];
B = [[0, 1], [2, 3], [4, 5]];
C = A .+ B;

D = zeros(5);
C = A .+ D;

x = 0;
y = 0.2;
z = "string";
print x, y, z;

# toDo:
# jakbym dal print A;, to wgl zle jest bo nie rozpoznaje typu A


# example of deleting variable after leaving scope:
{
	t = 5;
}
{
	t += 1;	
}
