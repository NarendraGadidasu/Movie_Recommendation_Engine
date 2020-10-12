
INSERT INTO Weights(Trope,Weight)
SELECT Trope, (1.0/count(Trope)) as weight  FROM all_movies
GROUP BY Trope
ORDER BY 2

UPDATE all_movies SET Weight = 
(SELECT weight FROM Weights WHERE all_movies.trope = Weights.trope) 
WHERE Trope IN (SELECT Trope FROM all_movies);
	 
	 
SELECT A.Movie as Movie_x, A.Trope as Trope_x, A.weight as weight_X ,B.Movie as Movie_y, B.Trope as Trope_y, B.weight as weight_y 
FROM all_movies A
INNER JOIN all_movies B ON A.Trope = B.Trope