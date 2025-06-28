(define (domain robot_guide_dishes_problem-domain)
  (:requirements :strips :typing :conditional-effects :negative-preconditions)

  (:types
    robot person cell dish chair
  )

  (:predicates
    (at_robot ?r - robot ?c - cell)
    (at_person ?p - person ?c - cell)
    (carrying_person ?r - robot ?p - person)
    (at_dish ?d - dish ?c - cell)
    (carrying_dish ?r - robot ?d - dish)
    (at_chair ?ch - chair ?c - cell)
    (dining_table ?c - cell)
    (adjacent ?c1 - cell ?c2 - cell)
    (passable ?c - cell)
    (occupies ?r - robot ?c - cell)
    (vegan_person ?p - person)
    (non_veg_person ?p - person)
    (vegan_dish ?d - dish)
    (non_veg_dish ?d - dish)
    (dish_served ?ch - chair ?d - dish)
  )

  (:action move
    :parameters (?r - robot ?from - cell ?to - cell)
    :precondition (and
      (at_robot ?r ?from)
      (adjacent ?from ?to)
      (passable ?to)
      (not (exists (?p - person) (at_person ?p ?to)))
      (not (exists (?d - dish) (at_dish ?d ?to)))
      (not (exists (?ch - chair) (at_chair ?ch ?to)))
      (not (exists (?c - cell) (and (dining_table ?c) (= ?c ?to))))
    )
    :effect (and
      (not (at_robot ?r ?from))
      (at_robot ?r ?to)
      (forall (?c - cell) (when (occupies ?r ?c) (not (occupies ?r ?c))))
      (occupies ?r ?to)
    )
  )

  (:action pick_up_person
    :parameters (?r - robot ?p - person ?c - cell)
    :precondition (and
      (at_robot ?r ?c)
      (at_person ?p ?c)
      (not (exists (?p2 - person) (carrying_person ?r ?p2)))
      (not (exists (?d - dish) (carrying_dish ?r ?d)))
    )
    :effect (and
      (not (at_person ?p ?c))
      (carrying_person ?r ?p)
    )
  )

  (:action drop_off_person
    :parameters (?r - robot ?p - person ?c - cell ?ch - chair)
    :precondition (and
      (at_robot ?r ?c)
      (carrying_person ?r ?p)
      (at_chair ?ch ?c)
      (not (exists (?p2 - person) (at_person ?p2 ?c)))
    )
    :effect (and
      (not (carrying_person ?r ?p))
      (at_person ?p ?c)
    )
  )

  (:action pick_up_dish
    :parameters (?r - robot ?d - dish ?c - cell)
    :precondition (and
      (at_robot ?r ?c)
      (at_dish ?d ?c)
      (not (exists (?p - person) (carrying_person ?r ?p)))
      (not (exists (?d2 - dish) (carrying_dish ?r ?d2)))
    )
    :effect (and
      (not (at_dish ?d ?c))
      (carrying_dish ?r ?d)
    )
  )

  (:action serve_dish
    :parameters (?r - robot ?d - dish ?c - cell ?ch - chair ?p - person)
    :precondition (and
      (at_robot ?r ?c)
      (carrying_dish ?r ?d)
      (at_chair ?ch ?c)
      (at_person ?p ?c)
      (or
        (and (vegan_person ?p) (vegan_dish ?d))
        (and (non_veg_person ?p) (non_veg_dish ?d))
      )
    )
    :effect (and
      (not (carrying_dish ?r ?d))
      (dish_served ?ch ?d)
    )
  )
)