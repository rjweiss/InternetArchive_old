db.congressmen.group(
                { key :
                        { 'congressman' : true },
                        initial : { sum : 0 },
                        reduce : function(doc, prev)
                                { prev.sum += 1 }
                }                
)

db.congressmen.distinct('congressman')
