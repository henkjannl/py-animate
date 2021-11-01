# Example 6: Bulldozer with bucket

![Moving bulldozer](bulldozer_bucket.gif)

In the main script, the global movement of the bulldozer, cloud and heap are still controlled by a `TABLE`. 

However, the bulldozer itself is now no longer an `IMAGE`, it has been replaced by an `ASSEMBLY` 'bulldozer'.

![Moving bulldozer main](Design/bulldozer_bucket_main.png)

The hierarchy of the animation is defined as follows:

![Bulldozer hierarchy](Design/bulldozer_bucket_hierarchy.png)

In the definition of the `ASSEMBLY` of the bulldozer, the bulldozer itself is drawn with the rotating wheel and bucket on it. 

The `ASSEMBLY` is made up of the following items:

![Bulldozer assembly items](Design/bulldozer_bucket_items.png)

Because the movements of the bucket and the wheel are quite simple, they are controlled within the 'Bulldozer' `SCRIPT`:

![Bulldozer assembly](Design/bulldozer_bucket_assembly.png)
